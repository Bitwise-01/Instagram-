# Date: 05/05/2018
# Author: Pure-L0G1C
# Description: Browser Manager 

from requests import Session
from .const import site_details
from .scraper import Scraper, Queue 

class Spyder(object):

 def __init__(self):
  self.proxy = None 
  self.isAlive = True 
  self.proxy_info = None
  self.proxies = Queue()
  self.scraper = Scraper()

 def proxy_manager(self):
  while self.isAlive:
   while all([self.isAlive, self.proxies.qsize]):pass 
   if not self.isAlive:break
   
   self.proxies = self.scraper.scrape(ssl_proxies=True)    
   [self.proxies.put(proxy) for proxy in self.scraper.scrape(new_proxies=True).queue if self.isAlive]

 @property
 def br(self):
  session = Session()
  session.proxies.update(self.proxy)
  session.headers.update(site_details['header'])
  return session 

 def renew_proxy(self, n=10):
  _proxy = self.proxies.get()
  addr = 'http://{}:{}'.format(_proxy['ip'], _proxy['port'])
  proxy = { 'http': addr, 'https': addr }
  
  if self.proxy:
   if all([self.proxy == proxy, self.proxies.qsize, n]):
    self.renew_proxy(n-1)
  self.proxy_info = _proxy
  self.proxy = proxy

 def ip_addr(self):
  try:
   return self.proxy['http'].split(':')[1][2:]
  except:pass 
