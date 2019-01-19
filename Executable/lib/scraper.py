# Date: 12/28/2018
# Author: Mohamed
# Description: Proxy scraper 

from time import sleep
from requests import get 
from .proxy import Proxy 
from .display import Display
from .proxy_list import ProxyList
from bs4 import BeautifulSoup as bs 
from threading import Thread, RLock


class Scraper(object):

    def __init__(self):
        self.lock = RLock()
        self.is_alive = True  
        self.display = Display()
        self.scraped_proxies = []
        self.extra_proxies_link = 'http://spys.me/proxy.txt'

        self.links = [
            'https://sslproxies.org', 
            'https://free-proxy-list.net',
            'https://free-proxy-list.net/anonymous-proxy.html'
        ]

    def parse_extra_proxy(self, proxy):
        proxy = proxy.split(' ')
        addr = proxy[0].split(':')

        return {
            'ip': addr[0],
            'port': addr[1],
            'country': proxy[1].split('-')[0]
        }        

    def parse_proxy(self, proxy):
        proxy = proxy.find_all('td')
        if proxy[4].string != 'transparent' and proxy[5].string != 'transparent':
            return { 
                'ip': proxy[0].string,
                'port': proxy[1].string,
                'country': proxy[3].string,
            }

    def scrape_proxies(self, link):
        proxies = [] 

        try:
            proxies = bs(get(link).text, 'html.parser').find('tbody').find_all('tr')
        except:
            pass 
        
        if not proxies:
            with self.lock:
                if self.is_alive:
                    self.display.warning('Failed to grab proxies from {}'.format(link))
        
        for proxy in proxies:
            with self.lock:
                _proxy = self.parse_proxy(proxy)
                if _proxy:
                    self.scraped_proxies.append(_proxy)
            
    def scrape_extra_proxies(self):
        proxies = [] 

        try:
            if self.is_alive:
                proxies = get(self.extra_proxies_link).text.split('\n')
        except:
            pass 
        
        if not proxies:
            with self.lock:
                if self.is_alive:
                    self.display.warning('Failed to grab proxies from {}'.format(self.extra_proxies_link))
        
        for proxy in proxies:
            if '-H' in proxy and '-S' in proxy:
                with self.lock:
                    self.scraped_proxies.append(self.parse_extra_proxy(proxy))                    
            
    @property
    def proxies(self):
        proxy_list = ProxyList()

        threads = []
        threads = [Thread(target=self.scrape_proxies, args=[link]) for link in self.links]
        threads.append(Thread(target=self.scrape_extra_proxies))
        
        for thread in threads:
            thread.daemon = True 
            thread.start()
        
        while self.is_alive and len(threads):
            for thread in [thread for thread in threads if not thread.is_alive()]:
                threads.pop(threads.index(thread))
            sleep(0.5)            
            
        if self.is_alive:
            for proxy in self.scraped_proxies:

                if not proxy in proxy_list:
                    proxy_list.append(Proxy(proxy))

        return proxy_list.list  