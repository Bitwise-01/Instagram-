'''
Date: 3/15/2019
Author: Mohamed
Description: Reads a file that contains a list of proxies and determines whether or not that list is good.
             Each line in the file must be in the format of ip:port
'''

import platform
from os import system
from time import sleep
from requests import Session
from threading import Thread, RLock

proxy_list = 'proxies.txt'
target_site = 'https://instagram.com'


def get_proxies():
    proxies = []

    with open(proxy_list, 'rt', encoding='utf-8') as proxies_file:

        for line in proxies_file:
            if not line:
                continue

            ip, port = line.replace('\r', '').split(':')

            port = int(port)
            proxy = {'ip': ip, 'port': port}
            proxies.append(proxy)

    return proxies


class TestProxies:

    def __init__(self, proxies):
        self.worked = 0
        self.failed = 0
        self.lock = RLock()
        self.active_brs = 0
        self.is_alive = True
        self.proxies = proxies
        self.total = len(proxies)
        self.test_link = target_site

    def display(self):
        system('cls' if platform.system() == 'Windows' else 'clear')
        worked, failed, total = self.worked, self.failed, self.total

        worked_per = round((worked/total) * 100, 2)
        failed_per = round((failed/total) * 100, 2)
        complete = round(worked_per + failed_per, 2)

        print(f'Complete: {complete}%')
        print(f'Active browsers: {self.active_brs}')
        print(f'Proxies worked: {worked_per}% [{worked}]')
        print(f'Proxies failed: {failed_per}% [{failed}]')

    def test_proxy(self, proxy):
        br = Session()

        addr = '{}:{}'.format(proxy['ip'], proxy['port'])
        addr = {'http': addr, 'https': addr}
        br.proxies.update(addr)

        try:
            br.get(self.test_link, timeout=(10, 15))

            with self.lock:
                self.worked += 1
        except:
            with self.lock:
                self.failed += 1
        finally:
            br.close()

            if self.is_alive:
                with self.lock:
                    self.display()

            self.active_brs -= 1

    def start(self):
        for proxy in self.proxies:

            while self.is_alive and self.active_brs >= 512:
                pass

            if not self.is_alive:
                break

            with self.lock:
                self.active_brs += 1

            Thread(target=self.test_proxy, args=[proxy], daemon=True).start()

        while self.is_alive and self.active_brs:
            sleep(0.5)

        self.display()

    def stop(self):
        self.is_alive = False

        while self.active_brs:
            try:
                with self.lock:
                    self.display()

                sleep(0.5)
            except KeyboardInterrupt:
                break

    def examine(self):
        failed = self.failed / self.total
        worked = self.worked / self.total

        if worked == 0:
            print('Bad proxy list')
        elif (failed - worked) >= 0.1:
            print('Bad proxy list')
        elif (failed - worked) == 0:
            print('Bad proxy list')
        else:
            print('Good proxy list')


if __name__ == '__main__':
    test_proxies = TestProxies(get_proxies())

    try:
        test_proxies.start()
    except KeyboardInterrupt:
        test_proxies.stop()
    finally:
        test_proxies.examine()
