# Date: 12/28/2018
# Author: Mohamed 
# Description: Password manager 

from time import sleep
from lib.display import Display


class PasswordManager(object):

    def __init__(self, passlist_path, max_passwords, session, resume):
        self.passlist = []
        self.is_alive = True 
        self.resume = resume
        self.is_read = False 
        self.session = session 
        self.passwords_removed = 0
        self.passlist_path = passlist_path
        self.max_passwords = max_passwords

    @property
    def list_size(self):
        return len(self.passlist)

    def list_add(self, password):
        if not password in self.passlist:
            self.passlist.append(password)
        
    def list_remove(self, password):
        if password in self.passlist:
            self.attempts += 1
            self.passlist.pop(self.passlist.index(password))
            self.session.write(self.attempts, self.passlist)
    
    def count_lines(self):
        lines = 0
        buffer = 1024 << 10

        with open(self.passlist_path, 'rb') as f:

            chunk = f.raw.read(buffer)

            while chunk:
                lines += chunk.count(b'\n')
                chunk = f.raw.read(buffer)
        
        return lines
    
    def read(self):
        attempts = 0
        Display.total_lines = self.count_lines()
        with open(self.passlist_path, 'rt', encoding='utf-8') as passlist:

            for password in passlist:
                if not self.is_alive:
                    break 
                
                if self.resume:
                    if attempts < (self.attempts + self.list_size):
                        attempts += 1
                        continue
                    else:
                        self.resume = False

                password = password.replace('\n', '').replace('\r', '').replace('\t', '')
                
                if self.list_size < self.max_passwords:
                    self.list_add(password)
                else:                    
                    while self.list_size >= self.max_passwords and self.is_alive:
                        sleep(0.5)
                    
                    if self.is_alive:
                        self.list_add(password)
                        self.session.write(self.attempts, self.passlist)

        if self.is_alive:
            self.is_read = True 
    
    @property
    def attempts(self):
        return self.passwords_removed
    
    @attempts.setter
    def attempts(self, n):
        self.passwords_removed = n
    
    def start(self):
        self.read()         
    
    def stop(self):
        self.is_alive = False