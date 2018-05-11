# Date: 05/03/2018
# Author: Pure-L0G1C
# Description: Proxy scraper

from requests import get
from .randqueue import Queue 
from bs4 import BeautifulSoup as bs 

class Scraper(object):

 def __init__(self):
  self.anony_proxis = 'https://free-proxy-list.net/anonymous-proxy.html'
  self.new_proxies = 'https://free-proxy-list.net'
  self.socks_proxies = 'https://socks-proxy.net'
  self.ssl_proxies = 'https://sslproxies.org'
  self.proxies  = Queue()
  self.isAlive  = False
  self.maxSize  = None

 def parse(self, proxy, ssl=False):
  if not self.isAlive:return 
  return {
          'ip': proxy[0].string, 'port': proxy[1].string,
          'protocol': 'SSL' if ssl else proxy[4].string, 
          'anonymity': proxy[4 if ssl else 5].string, 
          'country': proxy[3].string,
          'updated': proxy[7].string,
          'https': proxy[6].string
         }

 def fetch(self, url, ssl=False):
  try:proxies = bs(get(url).text, 'html.parser').find('tbody').findAll('tr')
  except KeyboardInterrupt:self.isAlive = False;return
  except:return
 
  for proxy in proxies:
   if not self.isAlive:break
   data = self.parse(proxy.findAll('td'), ssl)
   if data:
    if self.maxSize:
     if self.proxies.qsize < self.maxSize:
      self.proxies.put(data)
     else:break
    else:
     self.proxies.put(data)
 
 def scrape(self, size=None, new_proxies=False, anony_proxies=False, socks_proxies=False, ssl_proxies=False):
  self.proxies  = Queue()
  self.maxSize  = None
  self.isAlive  = True
  self.isAlive = True
  self.maxSize = size

  if all([self.isAlive, new_proxies]):
   self.fetch(self.new_proxies)

  if all([self.isAlive, anony_proxies]):
   self.fetch(self.anony_proxis)

  if all([self.isAlive, socks_proxies]):
   self.fetch(self.socks_proxies)

  if all([self.isAlive, ssl_proxies]):
   self.fetch(self.ssl_proxies, True)

  proxies = self.proxies
  self.proxies = Queue()
  return proxies