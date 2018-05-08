# Date: 05/03/2018
# Author: Pure-L0G1C
# Description: Proxy scraper

from requests import get
from bs4 import BeautifulSoup as bs 

class Queue(object):

 def __init__(self):
  self.queue = []
  
 def put(self, item):
  if not item in self.queue:
   self.queue.append(item)

 def get(self):
  if self.qsize:
   return self.queue.pop(0)
   
 @property 
 def qsize(self):
  return len(self.queue)

class Scraper(object):

 def __init__(self):
  self.anony_proxis = 'https://free-proxy-list.net/anonymous-proxy.html'
  self.new_proxies = 'https://free-proxy-list.net'
  self.socks_proxies = 'https://socks-proxy.net'
  self.ssl_proxies = 'https://sslproxies.org'
  self.isAlive  = False
  self.protocol = None
  self.country  = None
  self.proxies  = None
  self.maxSize  = None
  self.port =  None 

 def parse(self, proxy, ssl=False):
  if not self.isAlive:return 
  detail = {'ip': proxy[0].string, 'port': proxy[1].string,
            'protocol': 'SSL' if ssl else proxy[4].string, 
            'anonymity': proxy[4 if ssl else 5].string, 
            'country': proxy[3].string,
            'updated': proxy[7].string,
            'https': proxy[6].string}

  if all([self.protocol, self.country, self.port]):
   if detail['protocol'].lower() == self.protocol.lower():
    if detail['country'].lower() == self.country.lower():
     if detail['port'] == self.port:
      return detail
  elif all([self.protocol, self.country]):
   if detail['protocol'].lower() == self.protocol.lower():
    if detail['country'].lower() == self.country.lower():
     return detail
  elif all([self.protocol, self.port]):
   if detail['protocol'].lower() == self.protocol.lower():
    if detail['port'] == self.port:
     return detail
  elif all([self.country, self.port]):
   if detail['country'].lower() == self.country.lower():
    if detail['port'].lower() == self.port:
     return detail
  elif self.protocol:
   return None if detail['protocol'].lower() != self.protocol.lower() else detail
  elif self.country:
   return None if detail['country'].lower() != self.country.lower() else detail
  elif self.port:
   return None if detail['port'] != self.port else detail
  else:
   return detail

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
 
 def scrape(self, size=None, port=None, protocol=None, country=None, 
            new_proxies=False, anony_proxies=False, socks_proxies=False, ssl_proxies=False):
  self.port = str(port) if port else None 
  self.protocol = protocol
  self.country  = country
  self.proxies  = Queue()
  self.maxSize  = None
  self.isAlive  = True
  self.isAlive = True
  self.maxSize = size

  if protocol:
   if all([protocol.lower() != 'ssl', protocol.lower() != 'socks4', protocol.lower() != 'socks5']):
    print('Only Supporting SSL & Socks protocol')
    return 

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
