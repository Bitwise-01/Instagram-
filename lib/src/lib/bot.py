# Date: 05/10/2018
# Author: Pure-L0G1C
# Description: Proxy Bot

from .randqueue import Queue
from .const import MAX_REQUESTS

class Bot(object):
 
 def __init__(self, browser, url):
  self.url = url 
  self.br = browser
  self.requests = 0 
  self.isActive = False
  self.proxies = Queue()

 def parse_proxy(self, proxy):
  return {
   'ip': proxy['ip'],
   'port': proxy['port'],
   'country': proxy['country'] 
  } if proxy['country'] else None

 def scrape(self):
  if self.isActive:return 
  try:
   self.requests += 1
   self.isActive = True 
   resp = self.br.get(self.url)

   if resp.status_code != 200:
    self.requests = MAX_REQUESTS
   else:
    proxy = self.parse_proxy(resp.json())
    if proxy:self.proxies.put(proxy)
  except:
   self.requests = MAX_REQUESTS 
  finally:
   self.isActive = False