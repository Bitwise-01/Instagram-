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