# Date: 05/10/2018
# Author: Pure-L0G1C
# Description: Random Queue

from random import randint

class Queue(object):

 def __init__(self):
  self.queue = []
  
 def put(self, item):
  if not item in self.queue:
   self.queue.append(item)

 def get(self):
  if self.qsize:
   n = randint(0, len(self.queue)-1)
   return self.queue.pop(n)
   
 @property 
 def qsize(self):
  return len(self.queue)