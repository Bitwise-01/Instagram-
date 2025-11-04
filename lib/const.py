# Date: 12/28/2018
# Author: Mohamed
# Description: Constants

import os
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text
from time import sleep

console = Console()

console.print(
    Panel.fit(
        Text("H4CK3R  C0NST4NTS  L0ADER", style="bold green"),
        border_style="green",
        padding=(1, 3),
        subtitle="[green]Initializing...[/green]"
    )
)

sleep(0.8)

user_agents = [
    "Googlebot/2.1 (+http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; bingbot/2.0;  http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (compatible; adidxbot/2.0;  http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (seoanalyzer; compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm) SitemapProbe",
    "Mozilla/5.0 (Windows Phone 8.1; ARM; Trident/7.0; Touch; rv:11.0; IEMobile/11.0; NOKIA; Lumia 530) like Gecko (compatible; adidxbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53 (compatible; adidxbot/2.0;  http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53 (compatible; adidxbot/2.0; +http://www.bing.com/bingbot.htm)",
]

header = {
    "x-ig-app-id": "936619743392459",
    "x-instagram-ajax": "2f6bf8b37c04",
    "x-requested-with": "XMLHttpRequest",
    "referer": "https://www.instagram.com/",
    "content-type": "application/x-www-form-urlencoded",
}

username_field = "username"
password_field = "enc_password"
home_url = "https://www.instagram.com/"
login_url = "https://www.instagram.com/accounts/login/ajax/"

browser_data = {
    "header": header,
    "home_url": home_url,
    "login_url": login_url,
    "username_field": username_field,
    "password_field": password_field,
}

fetch_time = (10, 15)
response_codes = {"succeed": 0, "failed": 1, "locked": -1}

max_bad_proxies = 256
max_time_to_wait = 18
max_bots_per_proxy = 16

debug = False
credentials = "accounts.txt"
modes = {0: 512, 1: 256, 2: 128, 3: 64}

db_dir = "database"
db_database = "database.db"
db_path = os.path.join(db_dir, db_database)

if not os.path.exists(db_dir):
    os.mkdir(db_dir)

code_preview = """
Constants Summary
fetch_time      = (10, 15)
max_bad_proxies = 256
max_bots_per_proxy = 16
database_path   = "database/database.db"
"""

syntax = Syntax(code_preview, "python", theme="monokai", line_numbers=True, word_wrap=True)
console.print(Panel(syntax, title="[green]CONFIG PREVIEW[/green]", border_style="green"))

sleep(0.5)
console.print("[green]✔ All constants loaded successfully.[/green]")
console.print("[bold green]💻 System Ready. Initiating sequence...[/bold green]")
