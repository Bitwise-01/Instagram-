# Date: 12/28/2018
# Author: Mohamed
# Description: Proxy manager

import io
from time import sleep
from queue import Queue

from lib import database
from lib import proxy

import typing
import threading
import time

from requests_html import HTMLSession


class ProxyFinder:
    """Search online for publicly available proxies"""

    __fetch_interval_sec = 30 * 60  # 30 minutes
    __history_limit: int = 1024
    __http_proxies_url: str = "https://www.sslproxies.org/"
    __socks5_proxies_url: str = (
        "https://hidemy.name/en/proxy-list/?type=5#list"
    )

    def __init__(self):
        self.__history: typing.List[
            typing.Dict
        ] = []  # holds 1024 proxies at most
        self.proxies: typing.List[typing.Dict] = []
        self.last_updated: float = None

    def __add_proxy(self, proxy: typing.Dict) -> None:
        if proxy not in self.__history:
            self.__history.append(proxy)
            self.proxies.append(proxy)

        if len(self.__history) > self.__history_limit:
            self.__history.pop(0)

    def __get_socks_proxies(self) -> None:
        with HTMLSession() as session:
            r = session.get(self.__socks5_proxies_url)
            tr = r.html.find("table", first=True).find("tr")

            for row in tr[1:]:
                td = row.find("td")

                self.__add_proxy(
                    {
                        "ip": td[0].text,
                        "port": td[1].text,
                        "proxy_type": "socks5",
                    }
                )

    def __http_proxies(self) -> None:
        """Get proxies from http://www.sslproxies.org/"""

        with HTMLSession() as session:
            r = session.get(self.__http_proxies_url)
            table = r.html.find(".table", first=True)
            tr = table.find("tr")
            for row in tr[1:]:
                td = row.find("td")

                proxy = {
                    "ip": td[0].text,
                    "port": td[1].text,
                    "proxy_type": "http",
                }

                self.__add_proxy(proxy)

    def get_proxies(self) -> typing.List[typing.Optional[typing.Dict]]:
        """Get public proxies"""

        if self.last_updated is None:
            self.last_updated = time.time()
        else:
            if time.time() - self.last_updated < self.__fetch_interval_sec:
                return []

        # http proxies
        try:
            self.__http_proxies()
        except Exception as e:
            pass

        # socks5 proxies
        try:
            pass
            # self.__get_socks_proxies()
        except Exception as e:
            raise e
            pass

        self.last_updated = time.time()

        proxies = []
        size = len(self.proxies)

        for i in range(size):
            if i % 2:
                proxies.append(self.proxies.pop(0))
            else:
                proxies.append(self.proxies.pop())

        return proxies


class ProxyManager(object):
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
        """Read proxies from the file and write it into the database.

        File must contain ip:port format.
        Returns: Number of rows written into the database.
        """

        total_written = 0
        with io.open(proxylist_path, mode="rt", encoding="utf-8") as f:
            proxy = database.Proxy()

            for line in f:
                ip, port = line.split(":")

                ip = ip.strip()
                port = port.split()[0].strip()

                if proxy.add_proxy(ip=ip, port=port):
                    total_written += 1
        return total_written

    def dispose(self, proxy: proxy.Proxy) -> None:
        """Dispose of a proxy.

        A proxy will be updated after usage session.
        """

        info = proxy.info()
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
        """Add public proxies to the database"""

        for proxy in self.proxy_finder.get_proxies():
            self.db_proxy.add_proxy(
                ip=proxy.get("ip"),
                port=proxy.get("port"),
                proxy_type=proxy.get("proxy_type"),
            )

    def pop_list(self) -> None:
        """Populates queue using database"""

        self.add_public_proxies()

        proxies = self.db_proxy.get_proxies(
            self.__offset, self.__limit, min_score=self.__min_score
        )

        for proxy in proxies:
            basic_info = {
                "ip": proxy.get("ip"),
                "port": proxy.get("port"),
            }

            with self.lock_active_proxies:
                if basic_info in self.active_proxies:
                    continue

            last_used = proxy.get("last_used")

            if last_used:
                if time.time() - last_used <= self.__cooloff_period_seconds:
                    continue

            self.proxies.put(proxy)

            with self.lock_active_proxies:
                self.active_proxies.append(basic_info)

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
            return proxy.Proxy(p.get("ip"), p.get("port"), p.get("addr"))
