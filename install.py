# Date: 01/09/2019
# Author: Mohamed
# Description: Install file

from time import sleep
from queue import Queue 
from os.path import exists
from subprocess import Popen
from threading import Thread, RLock


class Install:

    def __init__(self, path_to_req): 
        self.lock = RLock()
        self.is_alive = True
        self.is_reading = True 
        self.is_installing = False 
        self.requirements = Queue()
        self.path_to_req = path_to_req
    
    @property 
    def path_exists(self):
        return exists(self.path_to_req)
    
    def read_file(self):
        with open('requirements.txt', mode='rt') as file: 
            for line in file:
                if line:
                    with self.lock:
                        self.requirements.put(line.replace('\n', ''))

        self.is_reading = False 

    def install(self, name):
        print('[+] Installing {} ...'.format(name))
        cmd = 'pip install {}'.format(name)
        cmd = cmd.split()

        try:
            self.is_installing = True 
            Popen(cmd).wait()
        except:
            print('[!] Failed to install {}'.format(name))
        finally:
            print('\n')
            self.is_installing = False 
    
    def install_all(self):
        while self.is_alive:

            while self.requirements.qsize():
                with self.lock:
                    name = self.requirements.get()
                self.install(name)

    def start_primary_threads(self):
        read_thread = Thread(target=self.read_file)
        install_all_thread = Thread(target=self.install_all)

        read_thread.daemon = True 
        install_all_thread.daemon = True 

        read_thread.start()
        install_all_thread.start()

    def start(self):
        if self.path_exists:
            self.start_primary_threads()

            while self.is_alive:

                try:
                    if not self.is_reading and not self.requirements.qsize() and not self.is_installing:
                        self.stop() 
                    sleep(0.5)
                except KeyboardInterrupt:
                    self.stop()             

        else:
            print('[*] Unable to locate the file requirements.txt') 
    
    def stop(self):
        self.is_alive = False 
    

if __name__ == '__main__':
    path_to_req = 'requirements.txt'

    install = Install(path_to_req)
    install.start()
