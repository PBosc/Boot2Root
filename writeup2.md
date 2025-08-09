Here we are going to try to exploit the binary with a rop chain

Before begining we do the same thing as in writeup1 until we get ssh connection to zaz.

First we find the libc version becaue there is not enought gadgets in the binary

libc is located at /lib/i386-linux-gnu/libc.so.6

It is in version 2.15

We download it with scp and run the script exploit-ROP.py to exploit a ROP chain

We are root !