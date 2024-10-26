ifconfig -a

-> vboxnet0 subnet => 192.168.56.0/24

nmap 192.168.56.0-255

Starting Nmap 7.80 ( https://nmap.org ) at 2024-10-26 20:10 CEST
Nmap scan report for paul-f4Ar6s7.clusters.42paris.fr (192.168.56.1)
Host is up (0.00013s latency).
Not shown: 995 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
111/tcp  open  rpcbind
2049/tcp open  nfs
5900/tcp open  vnc
9100/tcp open  jetdirect

Nmap scan report for 192.168.56.105
Host is up (0.0011s latency).
Not shown: 994 closed ports
PORT    STATE SERVICE
21/tcp  open  ftp
22/tcp  open  ssh
80/tcp  open  http
143/tcp open  imap
443/tcp open  https
993/tcp open  imaps


first one is our machine, second one is the vm

vm ip -> 192.168.56.105
http open
https open
ftp open
imap open

we run a kali docker to check the files on the server with dirb

docker pull kalilinux/kali-rolling
apt update
apt install -y dirb
dirb http://192.168.56.105 /usr/share/dirb/wordlists/common.txt

now we see there is an index, that give no info and a forum.

We try to view it with a web browser by going to https://192.168.56.105/forum/

in the forum, we find a long log file with multiple failed login attempts and then we see this line

Oct 5 08:45:29 BornToSecHackMe sshd[7547]: Failed password for invalid user !q\]Ej?*5K5cy*AJ from 161.202.39.38 port 57764 ssh2

this user is weird and looks like a password more than a user and we see that after that, there is a successful connexion to user lmezard so we think this is the password for this user (?)

ssh and ftp do not work with this user and password but we can login to the forum with it

we can find her name and e-mail laurie@borntosec.net

When we scanned the server ports with nmap, we saw a imap port which may tell us that a webmail is running.

We try to access this webmail server with lmezard's e-mail and the password we found before and it works.

We see 2 mails, one that seems to be really useful named "DB Access" and one named "Very Interesting"

In the mail we see :

```


Hey Laurie,

You cant connect to the databases now. Use root/Fg-'kKXBj87E:aJ$

Best regards.

```
so we now know how to connect to the db. We check if there is a phpmyadmin running and there is one and we can connect as root to it.

Connecting as root to the db is not the end though.