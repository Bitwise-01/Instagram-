# Date: 05/10/2018
# Author: Pure-L0G1C
# Description: Wrapper for gimme object

from .gimme import Gimme 

class Wrapper(object):
 
 def __init__(self, kwargs):
  self.gimme = Gimme(kwargs)

 @property
 def start(self):
  self.gimme.start()

 @property 
 def stop(self):
  self.gimme.stop()

 @property
 def get(self):
  return self.gimme.proxies.get()

 @property 
 def size(self):
  return self.gimme.proxies.lsize