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


class ProxyManager(object):
    __limit = 256
    __cooloff_period_seconds = 60

    def __init__(self):
        self.proxies = Queue()
        self.db_proxy = database.Proxy()
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

    def pop_list(self) -> None:
        """Populates queue using database"""

        proxies = self.db_proxy.get_proxies(
            self.__offset, self.__limit, min_score=self.__min_score
        )

        for proxy in proxies:
            basic_info = {"ip": proxy.get("ip"), "port": proxy.get("port")}

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
            return proxy.Proxy(p.get("ip"), p.get("port"))
