# Date: 05/05/2018
# Author: Pure-L0G1C
# Description: Browser Manager 

from .src.atom import Atom 
from requests import Session
from .const import fetch_time, site_details

class Spyder(object):

 def __init__(self):
  self.proxy = None 
  self.isAlive = True 
  self.proxy_info = None
  self.proxies = Atom(minSpeed=180)

 def proxy_manager(self):
  self.proxies.start()
  while self.isAlive:pass 
  self.proxies.stop()

 @property
 def br(self):
  session = Session()
  session.proxies.update(self.proxy)
  session.headers.update(site_details['header'])
  return session 

 def renew_proxy(self, n=10):
  _proxy = self.proxies.proxy
  proxy = { 'https': 'https://{}:{}'.format(_proxy['ip'], _proxy['port']) }

  if self.proxy:
   if all([self.proxy == proxy, self.proxies.size, n]):
    self.renew_proxy(n-1)
  self.proxy_info = _proxy
  self.proxy = proxy

 def ip_addr(self, br):
  try:
   return str(br.get('https://api.ipify.org/?format=text', timeout=fetch_time).text)
  except:pass 