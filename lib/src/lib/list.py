# Date: 05/10/2018
# Author: Pure-L0G1C
# Description: Active list

class List(object):
 ''' Prevents repeating data '''

 def __init__(self):
  self.list = []

 def add(self, item):
  if not item in self.list:
   self.list.append(item)

 def remove(self, index):
  del self.list[index]

 def get(self):
  ''' shrink list size '''
  if self.lsize:
   return self.list.pop(0)

 def get_item(self, index):
  ''' don't shrink list size '''
  return self.list[index]

 def get_index(self, item):
  return self.list.index(item)

 @property
 def lsize(self):
  return len(self.list)