# 12/29/2018
# Author: Mohamed 
# Description: Display 

from os import system
from time import sleep 
from .const import debug
from colorama import Fore 
from builtins import input
from platform import system as platform 


class Display(object):

    def __init__(self, username=None, passlist=None):
        self.delay = 1.3
        self.username = username
        self.passlist = passlist
        self.colors_disabled = True 
        self.cls = 'cls' if platform() == 'Windows' else 'clear'
        
    def clear(self):
        if not debug or self.colors_disabled:
            system(self.cls)

            if self.colors_disabled:
                self.colors_disabled = False 
        else:
            print('\n\n')           

    def stats(self, password, attempts, browsers, load=True):  
        self.clear()

        print('{0}[{1}-{0}] {1}Wordlist: {2}{3}{4}'.format(
            Fore.YELLOW, Fore.WHITE, Fore.CYAN, self.passlist, Fore.RESET
        ))

        print('{0}[{1}-{0}] {1}Username: {2}{3}{4}'.format(
            Fore.YELLOW, Fore.WHITE, Fore.CYAN, self.username.title(), Fore.RESET
        ))

        print('{0}[{1}-{0}] {1}Password: {2}{3}{4}'.format(
            Fore.YELLOW, Fore.WHITE, Fore.CYAN, password, Fore.RESET
        ))

        print('{0}[{1}-{0}] {1}Attempts: {2}{3}{4}'.format(
            Fore.YELLOW, Fore.WHITE, Fore.CYAN, attempts, Fore.RESET
        ))

        print('{0}[{1}-{0}] {1}Browsers: {2}{3}{4}'.format(
            Fore.YELLOW, Fore.WHITE, Fore.CYAN, browsers, Fore.RESET
        ))

        if load:
            sleep(self.delay)
    
    def stats_found(self, password, attempts, browsers):
        self.stats(password, attempts, browsers, load=False)
        
        print('\n{0}[{1}!{0}] {2}Password Found{3}'.format(
            Fore.YELLOW, Fore.RED, Fore.WHITE, Fore.RESET
        ))

        print('{0}[{1}+{0}] {2}Username: {1}{3}{4}'.format(
            Fore.YELLOW, Fore.GREEN, Fore.WHITE, self.username.title(), Fore.RESET
        ))

        print('{0}[{1}+{0}] {2}Password: {1}{3}{4}'.format(
            Fore.YELLOW, Fore.GREEN, Fore.WHITE, password, Fore.RESET
        ))
        
        sleep(self.delay)
    
    def stats_not_found(self, password, attempts, browsers):
        self.stats(password, attempts, browsers, load=False)        
        print('\n{0}[{1}!{0}] {2}Password Not Found{3}'.format(
            Fore.YELLOW, Fore.RED, Fore.WHITE, Fore.RESET
        ))

        sleep(self.delay)
    
    def shutdown(self, password, attempts, browsers):
        self.stats(password, attempts, browsers, load=False)
        print('\n{0}[{1}!{0}] {2}Shutting Down ...{3}'.format(
            Fore.YELLOW, Fore.RED, Fore.WHITE, Fore.RESET
        ))

        sleep(self.delay)
    
    def info(self, msg):
        self.clear()

        print('{0}[{1}i{0}] {2}{3}{4}'.format(
            Fore.YELLOW, Fore.CYAN, Fore.WHITE, msg, Fore.RESET
        ))

        sleep(2.5)
    
    def warning(self, msg):
        self.clear()

        print('{0}[{1}!{0}] {1}{2}{3}'.format(
            Fore.YELLOW, Fore.RED, msg, Fore.RESET
        ))

        sleep(self.delay)
    
    def prompt(self, data):
        self.clear()

        return input('{0}[{1}?{0}] {2}{3}{4}'.format(
            Fore.YELLOW, Fore.CYAN, Fore.WHITE, data, Fore.RESET
        ))