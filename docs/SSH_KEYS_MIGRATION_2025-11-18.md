# 🔐 SSH Keys Migration - Unification Project
**Datum:** 2025-11-18
**Důvod:** Kompromitace klíčů (pushnuty do public GitHub repo)

---

## 🎯 Cíl Migrace

1. **Vygenerovat nový unified ecosystem klíč** - nahradit kompromitované
2. **Distribuovat na všechny 4 stroje** (Aspire, HAS, LLMS, minipc)
3. **Zjistit stav Tailscale SSH** - zkontrolovat jestli není také kompromitovaný
4. **Unifikovat struktur**u - všechny klíče na stejných místech
5. **Otestovat konektivitu** - každý stroj s každým (12 spojení celkem)

---

## 📊 Inventura PŘED Migrací

### Stroje v Ecosystem:
| Název | IP Local | Tailscale IP | User | SSH Port |
|-------|----------|--------------|------|----------|
| **Aspire** (Workstation) | 192.168.0.10 | TBD | milhy777 | 2222 |
| **HAS** (Home Automation) | 192.168.0.58 | 100.79.142.112 | root | 2222 |
| **LLMS** (AI Server) | 192.168.0.41 | TBD | milhy777 | 2222 |
| **minipc** | TBD | TBD | TBD | 2222 |

---

## 🔍 Současný Stav Klíčů

### Aspire (Workstation):
```
Mapování probíhá...
```

### HAS:
```
Mapování probíhá...
```

### LLMS:
```
Mapování probíhá...
```

### minipc:
```
Mapování probíhá...
```

---

## 🔑 Nový Unified Klíč

**Typ:** ED25519 (moderní, bezpečný)
**Název:** `unified_ecosystem_key_2025`
**Komentář:** `unified-ecosystem-4pc-2025`

**Generování:**
```bash
ssh-keygen -t ed25519 \
  -f unified_ecosystem_key_2025 \
  -C "unified-ecosystem-4pc-2025" \
  -N ""
```

**Fingerprint:**
```
SHA256:vkf+bEwIL3JDX9fCx/MPfDNnVQi4932s9tlHy8/IfKo unified-ecosystem-4pc-2025 (ED25519)
```

**Vygenerováno:** 2025-11-18 (úspěšně)

---

## 📥 Distribuce

### 1. Aspire
- [ ] Zkopírovat klíč do `~/.ssh/`
- [ ] Přidat do `authorized_keys`
- [ ] Smazat starý kompromitovaný klíč
- [ ] Otestovat local konektivitu

### 2. HAS
- [ ] Zkopírovat klíč do `/root/.ssh/`
- [ ] Přidat do `authorized_keys`
- [ ] Zkopírovat do `/root/.ssh/ecosystem-keys/` (backup)
- [ ] Smazat starý klíč
- [ ] Otestovat konektivitu

### 3. LLMS
- [ ] Zkopírovat klíč do `~/.ssh/`
- [ ] Přidat do `authorized_keys`
- [ ] Smazat starý klíč
- [ ] Otestovat konektivitu

### 4. minipc
- [ ] Zkopírovat klíč do `~/.ssh/`
- [ ] Přidat do `authorized_keys`
- [ ] Smazat starý klíč
- [ ] Otestovat konektivitu

---

## 🧪 Testování Konektivity

### Matrix Test (12 spojení):
| From ↓ / To → | Aspire | HAS | LLMS | minipc |
|---------------|--------|-----|------|--------|
| **Aspire**    | -      | ⏳  | ⏳   | ⏳     |
| **HAS**       | ⏳     | -   | ⏳   | ⏳     |
| **LLMS**      | ⏳     | ⏳  | -    | ⏳     |
| **minipc**    | ⏳     | ⏳  | ⏳   | -      |

Legend: ⏳ Čeká | ✅ OK | ❌ Fail

---

## 🌐 Tailscale SSH Audit

### Tailscale Konfigurace:
```
Zjišťování...
```

### Tailscale Klíče:
```
Mapování probíhá...
```

---

## 📝 Finální Stav (PO Migraci)

Bude doplněno po dokončení...

---

*Migrace prováděna: Claude Code*
*Dokumentováno real-time během procesu*
