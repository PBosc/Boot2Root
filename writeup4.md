# Challenge – ret2shellcode (Shellcode in ENV)

## Étapes

### 1. Accès
Même procédure que dans **writeup1** jusqu’à obtenir l’accès à l’utilisateur `zaz`.

---

### 2. Exploit (shellcode via variable d’environnement)
Exploitation du binaire en injectant le shellcode **dans l’environnement** (au lieu d’appeler `system` depuis la libc).

```bash
python exploit-ret2shellcode.py
```

---

### Résultat
```
root@<target>#
```
Root obtenu ✅