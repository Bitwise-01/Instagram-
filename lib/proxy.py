# Date: 12/28/2018
# Author: Mohamed
# Description: Proxy

import time
import typing
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


class Proxy:
    def __init__(self, ip: str, port: int, addr: typing.Dict) -> None:
        self.__ip = ip
        self.__port = port
        self.__total_used = 0
        self.__total_passed = 0
        self.__last_used = None
        self.__addr = addr

    @property
    def addr(self) -> dict:
        self.__total_used += 1
        self.__last_used = time.time()
        return self.__addr

    def incr_success(self) -> None:
        self.__total_passed += 1
        console.print(Panel(f"[green]Proxy {self.__ip}:{self.__port} success incremented![/green]", border_style="green"))

    def decr_usage(self) -> None:
        self.__total_used = 0
        self.__total_passed = 0
        console.print(Panel(f"[green]Proxy {self.__ip}:{self.__port} usage reset[/green]", border_style="green"))

    def info(self) -> dict:
        table = Table(title=f"[green]Proxy Info: {self.__ip}:{self.__port}[/green]", border_style="green")
        table.add_column("Field", style="cyan", justify="right")
        table.add_column("Value", style="white", justify="left")
        table.add_row("IP", self.__ip)
        table.add_row("Port", str(self.__port))
        table.add_row("Last Used", str(self.__last_used) if self.__last_used else "Never")
        table.add_row("Total Used", str(self.__total_used))
        table.add_row("Total Passed", str(self.__total_passed))
        console.print(table)

        return {
            "ip": self.__ip,
            "port": self.__port,
            "last_used": self.__last_used,
            "total_used": self.__total_used,
            "total_passed": self.__total_passed,
        }
