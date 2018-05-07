# Date: 05/05/2018
# Author: Pure-L0G1C
# Description: Session Handler

from os import remove
from os.path import exists as path 
from csv import DictWriter, DictReader

class Session(object):
 def __init__(self, username, passlist):
  self.file = '.{}_{}.csv'.format(username, passlist.replace('\\', '_').replace('/', '_'))

 def exists(self):
  return path(self.file)

 def read(self):
  with open(self.file, 'r') as csvfile:
   session = DictReader(csvfile, delimiter = ',')
   try:return [_ for _ in session][0]
   except:pass 

 def write(self, attempts, queue):
  if not attempts:return
  with open(self.file, 'w') as csvfile:
   fieldnames = ['attempts', 'queue']
   writer = DictWriter(csvfile, fieldnames=fieldnames)

   writer.writeheader()
   writer.writerow({ 'attempts': attempts, 'queue': queue })

 def delete(self):
  if path(self.file):
   try:remove(self.file)
   except:pass 