# Date: 05/05/2018
# Author: Mohamed
# Description: Session Handler

from os import remove
from os.path import exists as path 
from csv import DictWriter, DictReader


class Session(object):

    is_busy = False

    def __init__(self, username, passlist):
        self.file = '.{}_{}.csv'.format(username, passlist.replace('\\', '_').replace('/', '_'))

    @property 
    def exists(self):
        return path(self.file)

    def read(self):
        with open(self.file, 'rt') as csvfile:
            session = DictReader(csvfile, delimiter = ',')
            try:return [_ for _ in session][0]
            except:pass 
    
    def _write(self, attempts, _list):
        with open(self.file, 'w') as csvfile:
            fieldnames = ['attempts', 'list']
            writer = DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({ 'attempts': attempts, 'list': _list })
        
    def write(self, attempts, _list):
        if not attempts:
            return
        
        while Session.is_busy:
            pass 
        
        try:
            Session.is_busy = True
            self._write(attempts, _list)
        except:
            pass 
        finally:
            Session.is_busy = False        
        
    def delete(self):
        if self.exists:
            try:
                remove(self.file) 
            except:
                pass 