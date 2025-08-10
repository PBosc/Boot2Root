# Boot VM to Root via init=/bin/sh

## Steps

### 1. Access to the boot terminal
- During VM startup, **spam the Shift key** to access the boot terminal.

---

### 2. Modify the boot line
At the prompt:
```bash
boot: live init=/bin/sh
```

---

### 3. Verify root access
Once the system has started:
```bash
whoami
```
Expected result:
```
root
```
Root access obtained ✅