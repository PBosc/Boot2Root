# Boot2Root - Bonus Challenge 6: Boot VM to Root via init=/bin/sh

## 1. Challenge Overview
**Challenge:** Boot VM to Root via init=/bin/sh

---

## 2. Steps

### 2.1 Access to the boot terminal
- During VM startup, **spam the Shift key** to access the boot terminal.

---

### 2.2 Modify the boot line
At the prompt:
```bash
boot: live init=/bin/sh
```

---

### 2.3 Verify root access
Once the system has started:
```bash
whoami
```

**Expected result:**
```
root
```

---

## 3. Result
**Root access obtained** ✅