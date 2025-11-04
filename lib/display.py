# 12/29/2018
# Author: Mohamed
# Description: Display

from os import system
from time import sleep
from .const import debug
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from platform import system as platform

console = Console()

class Display:

    __is_color = None
    total_lines = None
    account_exists = None

    def __init__(self, username=None, passlist=None, is_color=None):
        self.delay = 1.3
        self.username = username
        self.passlist = passlist
        self.colors_disabled = True
        self.cls = "cls" if platform() == "Windows" else "clear"

        if Display.__is_color is None:
            Display.__is_color = is_color

    def clear(self):
        if not debug or self.colors_disabled:
            system(self.cls)
            if self.colors_disabled and self.__is_color:
                self.colors_disabled = False
        else:
            console.print("\n\n")

    def stats(self, password, attempts, browsers, load=True):
        self.clear()
        complete = round((attempts / Display.total_lines) * 100, 2)
        account_exists = self.account_exists if self.account_exists is not None else ""

        if self.__is_color:
            panel_text = (
                f"[cyan]Wordlist:[/cyan] {self.passlist}\n"
                f"[cyan]Username:[/cyan] {self.username.title()}\n"
                f"[cyan]Password:[/cyan] {password}\n"
                f"[cyan]Complete:[/cyan] {complete}%\n"
                f"[cyan]Attempts:[/cyan] {attempts}\n"
                f"[cyan]Browsers:[/cyan] {browsers}\n"
                f"[cyan]Exists:[/cyan] {account_exists}"
            )
            console.print(Panel(panel_text, title="[green]H4CK3R STATS[/green]", border_style="green"))
        else:
            console.print(
                f"[-] Wordlist: {self.passlist}\n[-] Username: {self.username}\n[-] Password: {password}\n"
                f"Complete: {complete}\n[-] Attempts: {attempts}\n[-] Browsers: {browsers}\n[-] Exists: {account_exists}"
            )

        if load:
            sleep(self.delay)

    def stats_found(self, password, attempts, browsers):
        self.stats(password, attempts, browsers, load=False)
        if self.__is_color:
            panel_text = (
                f"[white]{self.username.title()}[/white]\n[green]{password}[/green]"
            )
            console.print(Panel(panel_text, title="[red]! Password Found[/red]", border_style="green"))
        else:
            console.print(f"\n[!] Password Found\n[+] Username: {self.username.title()}\n[+] Password: {password}")
        sleep(self.delay)

    def stats_not_found(self, password, attempts, browsers):
        self.stats(password, attempts, browsers, load=False)
        if self.__is_color:
            console.print(Panel("[red]! Password Not Found[/red]", border_style="green"))
        else:
            console.print("\n[!] Password Not Found")
        sleep(self.delay)

    def shutdown(self, password, attempts, browsers):
        self.stats(password, attempts, browsers, load=False)
        if self.__is_color:
            console.print(Panel("[red]! Shutting Down ...[/red]", border_style="green"))
        else:
            console.print("\n[!] Shutting Down ...")
        sleep(self.delay)

    def info(self, msg):
        self.clear()
        if self.__is_color:
            console.print(Panel(msg, title="[cyan]i[/cyan]", border_style="green"))
        else:
            console.print(f"[i] {msg}")
        sleep(2.5)

    def warning(self, msg):
        self.clear()
        if self.__is_color:
            console.print(Panel(msg, title="[red]![/red]", border_style="green"))
        else:
            console.print(f"[!] {msg}")
        sleep(self.delay)

    def prompt(self, data):
        self.clear()
        if self.__is_color:
            return Prompt.ask(f"[cyan]?[/cyan] {data}", console=console)
        else:
            return input(f"[?] {data}")
