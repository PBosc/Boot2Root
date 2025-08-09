## VirtualBox setup
You will need to create Network Manager (Host-Only Adapter).
On VirtualBox homepage, do File > Tools > Network Manager (Ctrl + H for short), then click Create.
Then, setup the VM with the B2R ISO, and go to the Settings of the VM. Click Network > Adapter 1, set "Attached to" to "Host-only Adapter". Make sure that name is the name of the virtual network you created previsouly (likely `vboxnet0`).

## Finding the IP
After the VM booted, run `ifconfig`.
Search out for the subnetwork you created in the previous step, and look for the `inet` value. We will take IP `192.168.56.1` for the demo.
Then, run [`nmap`](https://nmap.org/) on the network address (the address of the subnetwork that finishes with a 0), here: `192.168.56.0`.
Then run `nmap -sn 192.168.56.0/24` (skip ping scan, only do host discovery, network mask value indicated in the `inet` field).
You'll get an online host, we'll take IP `192.168.56.101` for the demo. 

To make sure that you found the right IP, navigate to `http://192.168.56.101`, you should see the website of the B2R CTF.