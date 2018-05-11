# Date: 05/10/2018
# Author: Pure-L0G1C
# Description: Gimme proxy scraper

from .spyder import Spyder
from .const import PROXY_URL
from threading import Thread 
from .manager import List, Manager 

class Gimme(object):

 def __init__(self, kwargs):
  self.size = kwargs['size'] if 'size' in kwargs else 50
  threads = kwargs['threads'] if 'threads' in kwargs else 50
  minSpeed = kwargs['minSpeed'] if 'minSpeed' in kwargs else 50
  protocol = kwargs['protocol'] if 'protocol' in kwargs else 'http'
  self.threads = threads if all([threads <= 50, threads > 0]) else 50
  self.isAlive = True
  self.proxies = List() 
  protocol = protocol.lower()
  protocol = protocol if any([protocol == 'http', 
                              protocol == 'socks4',
                              protocol == 'socks5']) else 'http'
  url = PROXY_URL.format(minSpeed, protocol)
  self.bot_manager = Manager(self.threads, url)

 def scrape_manager(self):
  while self.isAlive:
   while all([self.isAlive, self.proxies.lsize]):pass 
   if self.isAlive:
    try:
     while all([self.isAlive, self.proxies.lsize < self.size]):
      for _ in reversed(range(self.bot_manager.bots.lsize)):
       try:
        bot = self.bot_manager.bots.get_item(_)
        if not self.isAlive:break
        t = Thread(target=bot.scrape)
        t.daemon = True
        t.start()
       except:pass 
    except:pass
    
 def proxy_manager(self):
  while self.isAlive:
   try:
    while all([self.isAlive, self.proxies.lsize >= self.size]):pass
    for _ in reversed(range(self.bot_manager.bots.lsize)):
     try:
      bot = self.bot_manager.bots.get_item(_)
      if not self.isAlive:break
      if bot.proxies.qsize:
       if self.proxies.lsize < self.size:
        self.proxies.add(bot.proxies.get())
       else:break
     except:pass
   except:pass

 def start(self):
  proxy_manager = Thread(target=self.proxy_manager)
  scrape_manager = Thread(target=self.scrape_manager)

  proxy_manager.daemon = True 
  scrape_manager.daemon = True 

  proxy_manager.start()
  scrape_manager.start()
  self.bot_manager.start()

 def stop(self):
  self.isAlive = False 
  self.bot_manager.stop()