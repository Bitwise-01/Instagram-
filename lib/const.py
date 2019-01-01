# Date: 12/28/2018
# Author: Mohamed
# Description: Constants

# Browser
header = {
    'connection': 'close',
    'accept-language': 'en-US,en;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
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
fetch_time = (5, 10)
response_codes = { 'succeed': 0, 'failed': 1, 'locked': -1 }

# Limits
max_bad_proxies = 256
max_time_to_wait = 10
max_bots_per_proxy = 16

# Misc
debug = False
credentials = 'accounts.txt'
modes = { 0: 256, 1: 128, 2: 64, 3: 32 } 