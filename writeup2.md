# Boot2Root - ROP Chain Exploitation Writeup

## 1. Challenge Overview
**Challenge:** ROP Chain Exploitation

---

## 2. Steps

### 2.1 SSH connection to `zaz`
Proceed as in **writeup1** until you obtain SSH access.

---

### 2.2 Identify the `libc` version
```bash
ls -l /lib/i386-linux-gnu/libc.so.6
```

**Result:**
```
Version 2.15
```

---

### 2.3 Download the libc
```bash
scp zaz@<target-ip>:/lib/i386-linux-gnu/libc.so.6 .
```

---

### 2.4 Launch the ROP exploit
```bash
python exploit-ROP.py
```

---

## 3. Result
```
root@<target>#
```

**Root access obtained** ✅