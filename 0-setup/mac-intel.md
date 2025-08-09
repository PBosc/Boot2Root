### VM Configuration
Configure the VM normally. 
Before booting, go to Your VM > Network > Adapter 1
Choose Bridged Adapter, pick the interface your connected to (`en0: Wifi` if in WiFi or `eth0` if ethernet)
Boot the VM

### Finding the VM
Since the VM itself doesn't give its IP away, we need to find it. First, run `ifconfig` to get the status of your network interfaces:
```
ifconfig
...
en0: flags=8b63<UP,BROADCAST,SMART,RUNNING,PROMISC,ALLMULTI,SIMPLEX,MULTICAST> mtu 1500
	options=6460<TSO4,TSO6,CHANNEL_IO,PARTIAL_CSUM,ZEROINVERT_CSUM>
	ether 1a:f5:ba:5b:f8:a5
	inet6 fe80::453:fbe2:e8af:590c%en0 prefixlen 64 secured scopeid 0x7
	inet 10.80.248.234 netmask 0xffff0000 broadcast 10.80.255.255
	nd6 options=201<PERFORMNUD,DAD>
	media: autoselect
	status: active
...
```
Which gives away IP `10.80.248.234`. Then, we launch [[Nmap]] to discover all host under that IP mask
```
➜  ~ nmap -sn 10.80.248.234/24
Starting Nmap 7.94 ( https://nmap.org ) at 2025-06-28 15:32 CEST
Nmap scan report for 10.80.248.231
Host is up (0.0012s latency).
Nmap scan report for 10.80.248.234
Host is up (0.00050s latency).
Nmap done: 256 IP addresses (2 hosts up) scanned in 67.33 seconds
```
We test on the different IPs to see if they have open ports:
```
➜  ~ sudo nmap -sS -sV -O 10.80.248.231

Password:
Starting Nmap 7.94 ( https://nmap.org ) at 2025-06-28 15:33 CEST
Nmap scan report for 10.80.248.231
Host is up (0.00071s latency).
Not shown: 994 closed tcp ports (reset)
PORT    STATE SERVICE  VERSION
21/tcp  open  ftp      vsftpd 2.0.8 or later
22/tcp  open  ssh      OpenSSH 5.9p1 Debian 5ubuntu1.7 (Ubuntu Linux; protocol 2.0)
80/tcp  open  http     Apache httpd 2.2.22 ((Ubuntu))
143/tcp open  imap     Dovecot imapd
443/tcp open  ssl/http Apache httpd 2.2.22
993/tcp open  ssl/imap Dovecot imapd
MAC Address: 08:00:27:B0:81:09 (Oracle VirtualBox virtual NIC)
Device type: general purpose
Running: Linux 3.X
OS CPE: cpe:/o:linux:linux_kernel:3
OS details: Linux 3.2 - 3.16
Network Distance: 1 hop
Service Info: Host: 127.0.1.1; OS: Linux; CPE: cpe:/o:linux:linux_kernel

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 14.53 seconds
```
This one has, we found the VM

### Accessing the VM in SSH
We start [[Nmap]] in attack mode to have a better understanding:
```
➜  ~ sudo nmap -A 10.80.248.231

Starting Nmap 7.94 ( https://nmap.org ) at 2025-06-28 15:34 CEST
Nmap scan report for 10.80.248.231
Host is up (0.00093s latency).
Not shown: 994 closed tcp ports (reset)
PORT    STATE SERVICE  VERSION
21/tcp  open  ftp      vsftpd 2.0.8 or later
|_ftp-anon: got code 500 "OOPS: vsftpd: refusing to run with writable root inside chroot()".
22/tcp  open  ssh      OpenSSH 5.9p1 Debian 5ubuntu1.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   1024 07:bf:02:20:f0:8a:c8:48:1e:fc:41:ae:a4:46:fa:25 (DSA)
|   2048 26:dd:80:a3:df:c4:4b:53:1e:53:42:46:ef:6e:30:b2 (RSA)
|_  256 cf:c3:8c:31:d7:47:7c:84:e2:d2:16:31:b2:8e:63:a7 (ECDSA)
80/tcp  open  http     Apache httpd 2.2.22 ((Ubuntu))
|_http-server-header: Apache/2.2.22 (Ubuntu)
|_http-title: Hack me if you can
143/tcp open  imap     Dovecot imapd
|_ssl-date: 2025-06-28T13:34:39+00:00; 0s from scanner time.
| ssl-cert: Subject: commonName=localhost/organizationName=Dovecot mail server
| Not valid before: 2015-10-08T20:57:30
|_Not valid after:  2025-10-07T20:57:30
|_imap-capabilities: LITERAL+ capabilities more LOGINDISABLEDA0001 Pre-login IDLE ID STARTTLS have SASL-IR LOGIN-REFERRALS post-login ENABLE listed IMAP4rev1 OK
443/tcp open  ssl/http Apache httpd 2.2.22
|_ssl-date: 2025-06-28T13:34:39+00:00; 0s from scanner time.
|_http-server-header: Apache/2.2.22 (Ubuntu)
| ssl-cert: Subject: commonName=BornToSec
| Not valid before: 2015-10-08T00:19:46
|_Not valid after:  2025-10-05T00:19:46
|_http-title: 404 Not Found
993/tcp open  ssl/imap Dovecot imapd
| ssl-cert: Subject: commonName=localhost/organizationName=Dovecot mail server
| Not valid before: 2015-10-08T20:57:30
|_Not valid after:  2025-10-07T20:57:30
|_imap-capabilities: LITERAL+ capabilities more AUTH=PLAINA0001 IDLE IMAP4rev1 have post-login SASL-IR LOGIN-REFERRALS ENABLE Pre-login listed ID OK
|_ssl-date: 2025-06-28T13:34:39+00:00; 0s from scanner time.
MAC Address: 08:00:27:B0:81:09 (Oracle VirtualBox virtual NIC)
Device type: general purpose
Running: Linux 3.X
OS CPE: cpe:/o:linux:linux_kernel:3
OS details: Linux 3.2 - 3.16
Network Distance: 1 hop
Service Info: Host: 127.0.1.1; OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE
HOP RTT     ADDRESS
1   0.93 ms 10.80.248.231

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 15.56 seconds
```

#### Nmap Analysis
There are multiple services running:
- FTP server: port 21
- SSH server: port 22
- HTTP/S server: port 80/443
- IMAP server: port 143
- SSL/IMAP server: port 993

#### Website analysis
The website seems somewhat empty. Using [[Gobuster]] with [SecLists](https://github.com/danielmiessler/SecLists)' Common Directory, we get:
```
➜  wordlists gobuster dir -u http://10.80.248.231 -w SecLists/Discovery/Web-Content/common.txt -t 50

===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.80.248.231
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                SecLists/Discovery/Web-Content/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess            (Status: 403) [Size: 290]
/.hta                 (Status: 403) [Size: 285]
/cgi-bin/             (Status: 403) [Size: 289]
/.htpasswd            (Status: 403) [Size: 290]
/fonts                (Status: 301) [Size: 314] [--> http://10.80.248.231/fonts/]
/forum                (Status: 403) [Size: 286]
/index.html           (Status: 200) [Size: 1025]
/server-status        (Status: 403) [Size: 294]
Progress: 4727 / 4727 (100.00%)
===============================================================
Finished
===============================================================
```