# Boot VM to Root via init=/bin/sh

## Étapes

### 1. Accès au terminal de boot
- Pendant le lancement de la VM, **spammer la touche Shift** pour accéder au terminal de boot.

---

### 2. Modifier la ligne de boot
Au prompt :
```bash
boot: live init=/bin/sh
```

---

### 3. Vérifier l’accès root
Une fois le système démarré :
```bash
whoami
```
Résultat attendu :
```
root
```
Accès root obtenu ✅