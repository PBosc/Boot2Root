# Challenge – ROP Chain Exploitation

## Steps

### 1. SSH connection to `zaz`
Proceed as in **writeup1** until you obtain SSH access.

---

### 2. Identify the `libc` version
```bash
ls -l /lib/i386-linux-gnu/libc.so.6
```
Result:
```
Version 2.15
```

---

### 3. Download the libc
```bash
scp zaz@<target-ip>:/lib/i386-linux-gnu/libc.so.6 .
```

---

### 4. Launch the ROP exploit
```bash
python exploit-ROP.py
```

---

### Result
```
root@<target>#
```
Root access obtained ✅