# Challenge – Exploitation par ROP Chain

## Étapes

### 1. Connexion SSH à `zaz`
Procéder comme dans **writeup1** jusqu’à obtenir l’accès SSH.

---

### 2. Identifier la version de `libc`
```bash
ls -l /lib/i386-linux-gnu/libc.so.6
```
Résultat :
```
Version 2.15
```

---

### 3. Télécharger la libc
```bash
scp zaz@<target-ip>:/lib/i386-linux-gnu/libc.so.6 .
```

---

### 4. Lancer l’exploit ROP
```bash
python exploit-ROP.py
```

---

### Résultat
```
root@<target>#
```
Accès root obtenu ✅