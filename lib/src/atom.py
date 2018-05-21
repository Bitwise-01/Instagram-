# Date: 05/09/2018
# Author: Pure-L0G1C
# Description: Gimme proxies

from .lib.wrap import Wrapper

class Atom(object):

 def __init__(self, **kwargs):
  self.proxies = Wrapper(kwargs)  

 def start(self):
  self.proxies.start

 def stop(self):
  self.proxies.stop

 @property 
 def size(self):
  return self.proxies.size 

 @property 
 def proxy(self):
  return self.proxies.get
