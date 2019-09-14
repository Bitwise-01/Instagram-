# Date: 12/28/2018
# Author: Mohamed
# Description: Constants

import os

# Browser
header = {
    'x-ig-app-id': '936619743392459',
    'x-instagram-ajax': '2f6bf8b37c04',
    'x-requested-with': 'XMLHttpRequest',
    'referer': 'https://www.instagram.com/',
    'content-type': 'application/x-www-form-urlencoded'
}

username_field = 'username'
password_field = 'password'
home_url = 'https://www.instagram.com/'
login_url = 'https://www.instagram.com/accounts/login/ajax/'

browser_data = {
    'header': header,
    'home_url': home_url,
    'login_url': login_url,
    'username_field': username_field,
    'password_field': password_field
}

# Login
fetch_time = (10, 15)
response_codes = {'succeed': 0, 'failed': 1, 'locked': -1}

# Limits
max_bad_proxies = 128
max_time_to_wait = 18
max_bots_per_proxy = 16

# Misc
debug = False
credentials = 'accounts.txt'
modes = {0: 512, 1: 256, 2: 128, 3: 64}

# Database
db_dir = 'database'
db_session = 'session.db'
db_path = os.path.join(db_dir, db_session)

if not os.path.exists(db_dir):
    os.mkdir(db_dir)
