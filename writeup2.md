Here we are going to try to exploit the binary with a rop chain

first we find the libc version becaue there is not enought gadgets in the binary


libc is located at /lib/i386-linux-gnu/libc.so.6

it is in version 2.15

we download it with scp and run the script exploit-ROP.py to exploit a ROP chain
