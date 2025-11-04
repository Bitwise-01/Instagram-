import io
import threading
import time
import typing
from queue import Queue
from time import sleep
from requests_html import HTMLSession
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.text import Text

from lib import database
from lib import proxy

console = Console()


class ProxyFinder:
    __fetch_interval_sec = 30 * 60
    __history_limit: int = 1024
    __http_proxies_url: str = "https://www.sslproxies.org/"
    __socks5_proxies_url: str = "https://hidemy.name/en/proxy-list/?type=5#list"

    def __init__(self):
        self.__history: typing.List[typing.Dict] = []
        self.proxies: typing.List[typing.Dict] = []
        self.last_updated: float = None

    def __add_proxy(self, proxy_dict: typing.Dict) -> None:
        if proxy_dict not in self.__history:
            self.__history.append(proxy_dict)
            self.proxies.append(proxy_dict)
        if len(self.__history) > self.__history_limit:
            self.__history.pop(0)

    def __http_proxies(self) -> None:
        with HTMLSession() as session:
            r = session.get(self.__http_proxies_url)
            table = r.html.find(".table", first=True)
            tr = table.find("tr")
            for row in tr[1:]:
                td = row.find("td")
                self.__add_proxy({
                    "ip": td[0].text,
                    "port": td[1].text,
                    "proxy_type": "http",
                })

    def get_proxies(self) -> typing.List[typing.Optional[typing.Dict]]:
        if self.last_updated is None:
            self.last_updated = time.time()
        elif time.time() - self.last_updated < self.__fetch_interval_sec:
            return []

        try:
            self.__http_proxies()
            console.print(Panel("[green]HTTP proxies fetched successfully[/green]", border_style="green"))
        except Exception:
            console.print(Panel("[red]! Failed to fetch HTTP proxies[/red]", border_style="green"))

        self.last_updated = time.time()
        proxies = []
        size = len(self.proxies)
        for i in range(size):
            if i % 2:
                proxies.append(self.proxies.pop(0))
            else:
                proxies.append(self.proxies.pop())
        return proxies


class ProxyManager:
    __limit = 256
    __cooloff_period_seconds = 60

    def __init__(self):
        self.proxies = Queue()
        self.db_proxy = database.Proxy()
        self.proxy_finder = ProxyFinder()
        self.active_proxies: typing.List[dict] = []
        self.lock_active_proxies = threading.RLock()
        self.__offset: int = 0
        self.__limit: int = 256
        self.__min_score: float = 0.0

    def write2db(self, proxylist_path: str) -> int:
        total_written = 0
        with io.open(proxylist_path, mode="rt", encoding="utf-8") as f:
            proxy_db = database.Proxy()
            for line in f:
                ip, port = line.split(":")
                ip = ip.strip()
                port = port.split()[0].strip()
                if proxy_db.add_proxy(ip=ip, port=port):
                    total_written += 1
        console.print(Panel(f"[green]Proxies written to DB: {total_written}[/green]", border_style="green"))
        return total_written

    def dispose(self, proxy_obj: proxy.Proxy) -> None:
        info = proxy_obj.info()
        basic_info = {"ip": info.get("ip"), "port": info.get("port")}
        if info.get("total_used"):
            self.db_proxy.update_status(
                info.get("ip"),
                info.get("port"),
                info.get("last_used"),
                info.get("total_used") or 0,
                info.get("total_passed") or 0,
            )
        with self.lock_active_proxies:
            if basic_info in self.active_proxies:
                self.active_proxies.remove(basic_info)

    def add_public_proxies(self) -> None:
        proxies = self.proxy_finder.get_proxies()
        if proxies:
            with Progress(
                SpinnerColumn(spinner_name="dots"),
                "[progress.description]{task.description}",
                BarColumn(bar_width=None, complete_style="green"),
                TextColumn("[green]{task.completed}/{task.total} proxies added[/green]"),
                console=console,
            ) as progress:
                task = progress.add_task("[green]Adding public proxies...[/green]", total=len(proxies))
                for proxy_dict in proxies:
                    self.db_proxy.add_proxy(
                        ip=proxy_dict.get("ip"),
                        port=proxy_dict.get("port"),
                        proxy_type=proxy_dict.get("proxy_type"),
                    )
                    progress.update(task, advance=1)
                    sleep(0.05)

    def pop_list(self) -> None:
        self.add_public_proxies()
        proxies = self.db_proxy.get_proxies(self.__offset, self.__limit, min_score=self.__min_score)
        with Progress(
            SpinnerColumn(),
            "[progress.description]{task.description}",
            BarColumn(bar_width=None, complete_style="green"),
            TextColumn("[green]{task.completed}/{task.total} proxies queued[/green]"),
            console=console,
        ) as progress:
            task = progress.add_task("[green]Populating proxy queue...[/green]", total=len(proxies))
            for proxy_dict in proxies:
                basic_info = {"ip": proxy_dict.get("ip"), "port": proxy_dict.get("port")}
                with self.lock_active_proxies:
                    if basic_info in self.active_proxies:
                        progress.update(task, advance=1)
                        continue
                last_used = proxy_dict.get("last_used")
                if last_used and time.time() - last_used <= self.__cooloff_period_seconds:
                    progress.update(task, advance=1)
                    continue
                self.proxies.put(proxy_dict)
                with self.lock_active_proxies:
                    self.active_proxies.append(basic_info)
                progress.update(task, advance=1)
                sleep(0.01)

        if proxies:
            self.__offset += self.__limit
        else:
            self.__offset = 0
            self.__min_score = self.db_proxy.calc_q1()

    def get_proxy(self) -> typing.Union[proxy.Proxy, None]:
        if not self.proxies.qsize():
            self.pop_list()
        if self.proxies.qsize():
            p = self.proxies.get()
            console.print(Panel(f"[green]Proxy assigned: {p.get('ip')}:{p.get('port')}[/green]", border_style="green"))
            return proxy.Proxy(p.get("ip"), p.get("port"), p.get("addr"))
        return None
