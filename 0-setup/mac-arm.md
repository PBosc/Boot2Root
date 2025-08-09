We will need UTM for this demo.

# UTM setup
You need to **emulate** the machine since the ISO is x86_64 based and not ARM.
Then, once you properly configured the boot settings, select your VM on the left panel and click the "Settings" (the right-est icon on the top bar of UTM)(make sure your VM is not running, else you can't edit the settings)
Under the Network tab, set Network Mode to "Host Only", and in the emulated network card pick "Intel Gigabit Ethernet (e1000)". Save and boot the VM.
Wait for the VM to fully boot, you should be prompted with the login prompt.

# Finding the IP
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