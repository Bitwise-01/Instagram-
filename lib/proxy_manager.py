# Date: 12/28/2018
# Author: Mohamed
# Description: Proxy manager

from time import sleep
from queue import Queue
from .scraper import Scraper
from .bad_proxies import BadProxies


class ProxyManager(object):

    def __init__(self):
        self.is_alive = True
        self.proxies = Queue()
        self.scraper = Scraper()
        self.bad_proxies = BadProxies()

    def collect(self):
        while self.is_alive:
            if not self.proxies.qsize():

                for proxy in self.scraper.proxies:
                    if not proxy in self.bad_proxies:
                        self.proxies.put(proxy)

            sleep(5)

    def bad_proxy(self, proxy):
        if not proxy in self.bad_proxies:
            self.bad_proxies.append(proxy)

    def get_proxy(self):
        if self.proxies.qsize():
            return self.proxies.get()

    def start(self):
        self.collect()

    def stop(self):
        self.is_alive = False
        self.scraper.is_alive = False
