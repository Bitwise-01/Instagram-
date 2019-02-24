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

    __is_color = None 
    total_lines = None 
    account_exists = None 

    def __init__(self, username=None, passlist=None, is_color=None):
        self.delay = 1.3
        self.username = username
        self.passlist = passlist
        self.colors_disabled = True 
        self.cls = 'cls' if platform() == 'Windows' else 'clear'

        if Display.__is_color == None :
            Display.__is_color = is_color

    def clear(self):
        if not debug or self.colors_disabled:
            system(self.cls)

            if self.colors_disabled and self.__is_color:
                self.colors_disabled = False 
        else:
            print('\n\n')           

    def stats(self, password, attempts, browsers, load=True):  
        self.clear()
        complete = round((attempts/Display.total_lines) * 100, 2)
        account_exists = self.account_exists if self.account_exists != None else ''

        if self.__is_color:
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

            print('{0}[{1}-{0}] {1}Exists: {2}{3}{4}'.format(
                Fore.YELLOW, Fore.WHITE, Fore.CYAN, account_exists, Fore.RESET
            ))

            print('{0}[{1}-{0}] {1}Complete: {2}{3}%{4}'.format(
                Fore.YELLOW, Fore.WHITE, Fore.CYAN, complete, Fore.RESET
            ))

        else:            
            print('[-] Wordlist: {}\n[-] Username: {}\n[-] Password: {}\n[-] Attempts: {}\n[-] Browsers: {}\n[-] Exists: {}\n[-] Complete: {}%'.format(
                self.passlist, self.username, password, attempts, browsers, account_exists, complete
            ))

        if load:
            sleep(self.delay)
    
    def stats_found(self, password, attempts, browsers):
        self.stats(password, attempts, browsers, load=False)

        if self.__is_color:        
            print('\n{0}[{1}!{0}] {2}Password Found{3}'.format(
                Fore.YELLOW, Fore.RED, Fore.WHITE, Fore.RESET
            ))

            print('{0}[{1}+{0}] {2}Username: {1}{3}{4}'.format(
                Fore.YELLOW, Fore.GREEN, Fore.WHITE, self.username.title(), Fore.RESET
            ))

            print('{0}[{1}+{0}] {2}Password: {1}{3}{4}'.format(
                Fore.YELLOW, Fore.GREEN, Fore.WHITE, password, Fore.RESET
            ))
        else:
            print('\n[!] Password Found\n[+] Username: {}\n[+] Password: {}'.format(
                self.username.title(), password
            ))
        
        sleep(self.delay)
    
    def stats_not_found(self, password, attempts, browsers):
        self.stats(password, attempts, browsers, load=False)  

        if self.__is_color:      
            print('\n{0}[{1}!{0}] {2}Password Not Found{3}'.format(
                Fore.YELLOW, Fore.RED, Fore.WHITE, Fore.RESET
            ))
        else:
            print('\n[!] Password Not Found')

        sleep(self.delay)
    
    def shutdown(self, password, attempts, browsers):
        self.stats(password, attempts, browsers, load=False)

        if self.__is_color:
            print('\n{0}[{1}!{0}] {2}Shutting Down ...{3}'.format(
                Fore.YELLOW, Fore.RED, Fore.WHITE, Fore.RESET
            ))
        else:
            print('\n[!] Shutting Down ...')

        sleep(self.delay)
    
    def info(self, msg):
        self.clear()

        if self.__is_color:
            print('{0}[{1}i{0}] {2}{3}{4}'.format(
                Fore.YELLOW, Fore.CYAN, Fore.WHITE, msg, Fore.RESET
            ))
        else:
            print('[i] {}'.format(msg))

        sleep(2.5)
    
    def warning(self, msg):
        self.clear()

        if self.__is_color:
            print('{0}[{1}!{0}] {1}{2}{3}'.format(
                Fore.YELLOW, Fore.RED, msg, Fore.RESET
            ))
        else:
            print('[!] {}'.format(msg))

        sleep(self.delay)
    
    def prompt(self, data):
        self.clear()
        
        if self.__is_color:
            return input('{0}[{1}?{0}] {2}{3}{4}'.format(
                Fore.YELLOW, Fore.CYAN, Fore.WHITE, data, Fore.RESET
            ))
        else:
            return input('[?] {}'.format(data))