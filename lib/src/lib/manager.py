# Date: 05/10/2018
# Author: Pure-L0G1C
# Description: Manages bots

from .bot import Bot 
from .list import List 
from .spyder import Spyder
from threading import Thread  
from .const import MAX_REQUESTS

class Manager(object):
  
 def __init__(self, threads, url):
  self.threads = threads
  self.spyder = Spyder() 
  self.isAlive = True
  self.bots = List() 
  self.url = url 

 def bot_size_manager(self):
  while self.isAlive:
   while all([self.isAlive, self.bots.lsize < self.threads]):
    try:
     if self.spyder.proxies.qsize:
      proxy = self.spyder.proxies.get()
      proxy_addr = { 'https': 'https://{}:{}'.format(proxy['ip'], proxy['port']) }
      browser = self.spyder.browser(proxy_addr)
      bot = Bot(browser, self.url)
      self.bots.add(bot)
    except KeyboardInterrupt:
     self.isAlive = False

 def bot_requests_manager(self):
  while self.isAlive:
   while all([self.isAlive, self.bots.lsize]):
    try:
     expired = [] # expired bots 

     for _ in range(self.bots.lsize):
      bot = self.bots.get_item(_)
      if bot.requests >= MAX_REQUESTS:
       expired.append(_)

     for _ in expired:
      self.bots.remove(_)

    except KeyboardInterrupt:
     self.isAlive = False

 def start(self):
  bot_size = Thread(target=self.bot_size_manager)
  spyder = Thread(target=self.spyder.proxy_manager)
  bot_requests = Thread(target=self.bot_requests_manager)

  bot_requests.daemon = True
  bot_size.daemon = True
  spyder.daemon = True 

  spyder.start()
  bot_size.start()
  bot_requests.start()

 def stop(self):
  self.isAlive = False 
  self.spyder.isAlive = False 