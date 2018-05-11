# Date: 05/05/2018
# Author: Pure-L0G1C
# Description: Browser Manager 

from .scraper import Scraper
from requests import Session
from .randqueue import Queue 
from .const import HEADER_DETAILS

class Spyder(object):

 def __init__(self):
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

 def browser(self, proxy_addr):
  session = Session()
  session.proxies.update(proxy_addr)
  session.headers.update(HEADER_DETAILS)
  return session 