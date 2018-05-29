# Date: 05/05/2018
# Author: Pure-L0G1C
# Description: Consts

credentials = 'accounts.txt'

# limits 
max_fails = 8
fetch_time = (5, 10)
max_proxy_usage = 16

# Instagram's details
instagram_username_field = 'username'
instagram_password_field = 'password'
home_url = 'https://www.instagram.com/'
login_url = 'https://www.instagram.com/accounts/login/ajax/'

site_details = {
 'name':'Instagram',
 'home_url': home_url, 
 'login_url': login_url,
 'username_field': instagram_username_field,
 'password_field': instagram_password_field,
 'header': { 'Referer': 'https://www.instagram.com', 'Connection': 'close' }
 }