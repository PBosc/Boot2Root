# Boot2Root - Bonus Challenge 4: ret2shellcode (Shellcode in ENV)

## 1. Challenge Overview
**Challenge:** ret2shellcode - Shellcode injection via environment variable

---

## 2. Steps

### 2.1 Access
Same procedure as in **writeup1** until you obtain access to the `zaz` user.

---

### 2.2 Exploit (shellcode via environment variable)
Exploitation of the binary by injecting the shellcode **in the environment** (instead of calling `system` from libc).

```bash
python exploit-ret2shellcode.py
```

---

## 3. Result
```
root@<target>#
```

**Root obtained** ✅