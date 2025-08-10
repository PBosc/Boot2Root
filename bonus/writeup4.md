# Challenge – ret2shellcode (Shellcode in ENV)

## Steps

### 1. Access
Same procedure as in **writeup1** until you obtain access to the `zaz` user.

---

### 2. Exploit (shellcode via environment variable)
Exploitation of the binary by injecting the shellcode **in the environment** (instead of calling `system` from libc).

```bash
python exploit-ret2shellcode.py
```

---

### Result
```
root@<target>#
```
Root obtained ✅