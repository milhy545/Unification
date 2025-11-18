# 🔐 Proton Drive Backup Strategy pro SSH Klíče

## Přehled

SSH klíče `unified_ecosystem_key` jsou kryptograficky citlivé a vyžadují bezpečné záložní úložiště.

## Backup Strategie

### ✅ Primární Úložiště: HAS Server
- **Lokace:** `root@192.168.0.58:/root/.ssh/ecosystem-keys/`
- **Přístup:** Pouze přes SSH (port 2222)
- **Oprávnění:** chmod 600
- **Backup:** Automatický rsync do `/backup/ssh-keys/`

### ☁️ Cloud Backup: Proton Drive

#### Možnost 1: Manuální Upload (Nejjednodušší)

1. **Zašifruj klíče lokálně:**
   ```bash
   # Vytvoř šifrovaný archiv
   cd ~/Develop/Unification/ssh-keys-export

   # GPG šifrování
   tar czf - unified_ecosystem_key* README.md | \
     gpg --symmetric --cipher-algo AES256 \
     --output ssh-keys-backup-$(date +%Y%m%d).tar.gz.gpg

   # Nebo 7zip s AES-256
   7z a -p -mhe=on -mx=9 \
     ssh-keys-backup-$(date +%Y%m%d).7z \
     unified_ecosystem_key* README.md
   ```

2. **Upload do Proton Drive:**
   - Otevři https://drive.proton.me
   - Vytvoř složku: `Backups/SSH-Keys/`
   - Upload: `ssh-keys-backup-YYYYMMDD.tar.gz.gpg`
   - **Heslo uložit do Proton Pass!**

3. **Verifikace:**
   ```bash
   # Test dešifrování
   gpg --decrypt ssh-keys-backup-$(date +%Y%m%d).tar.gz.gpg | tar xz
   ```

#### Možnost 2: rclone (Automatizované)

**Setup:**
```bash
# Instalace rclone
curl https://rclone.org/install.sh | sudo bash

# Konfigurace Proton Drive
rclone config
# Vyber: Proton Drive
# Použij webauth flow
```

**Backup Script:**
```bash
#!/bin/bash
# Auto backup to Proton Drive

BACKUP_DIR="/tmp/ssh-keys-backup-$$"
DATE=$(date +%Y%m%d)

mkdir -p "$BACKUP_DIR"

# Vytvoř šifrovaný backup
tar czf - unified_ecosystem_key* README.md | \
  gpg --symmetric --cipher-algo AES256 \
  --passphrase-file ~/.ssh-backup-passphrase \
  --batch --yes \
  --output "$BACKUP_DIR/ssh-keys-backup-${DATE}.tar.gz.gpg"

# Upload do Proton Drive
rclone copy "$BACKUP_DIR/" protondrive:Backups/SSH-Keys/

# Cleanup
rm -rf "$BACKUP_DIR"
```

**Cronjob (měsíční backup):**
```bash
# Přidej do crontab
0 3 1 * * /home/milhy777/Develop/Unification/ssh-keys-export/proton-backup.sh
```

#### Možnost 3: Proton Drive Linux Client (Beta)

```bash
# Instalace
flatpak install flathub ch.protonmail.protondrive

# Mount
protondrive mount ~/ProtonDrive

# Automatický sync
cp ssh-keys-backup-*.gpg ~/ProtonDrive/Backups/SSH-Keys/
```

## 🔒 Security Best Practices

### Šifrování
- **VŽDY** šifruj klíče před uploadem do cloudu
- Použij AES-256 minimum
- Heslo uložit v Proton Pass (ne v plain text)

### Oprávnění
```bash
# Lokální backup soubory
chmod 600 ssh-keys-backup-*.gpg
chmod 700 ~/Backups/ssh-keys/
```

### Retence
- **Proton Drive:** Uložit poslední 12 měsíčních backupů
- **HAS:** Rolling backup (poslední 7 dní)
- **Lokální:** Žádné plain text backupy (pouze šifrované)

## 📝 Recovery Procedure

### Z Proton Drive:
```bash
# 1. Stáhni backup
rclone copy protondrive:Backups/SSH-Keys/ssh-keys-backup-YYYYMMDD.tar.gz.gpg ./

# 2. Dešifruj
gpg --decrypt ssh-keys-backup-YYYYMMDD.tar.gz.gpg | tar xz

# 3. Nastav oprávnění
chmod 600 unified_ecosystem_key
chmod 644 unified_ecosystem_key.pub

# 4. Upload na HAS
./upload-keys-to-has.sh
```

### Z HAS:
```bash
# Jednodušší - rovnou z HAS
./fetch-keys-from-has.sh
```

## 🗓️ Backup Schedule

| Zdroj | Cíl | Frekvence | Metoda |
|-------|-----|-----------|--------|
| Lokální | HAS | Při změně | `upload-keys-to-has.sh` |
| HAS | HAS `/backup/` | Denně | rsync (automaticky) |
| Lokální | Proton Drive | Měsíčně | rclone/manuální |
| HAS | Proton Drive | Kvartálně | Manuální export |

## ✅ Checklist

- [ ] Nastavit GPG heslo pro šifrování
- [ ] Uložit heslo do Proton Pass
- [ ] Vytvořit první šifrovaný backup
- [ ] Upload do Proton Drive složky `Backups/SSH-Keys/`
- [ ] Test recovery procedure
- [ ] (Optional) Nastavit rclone automatizaci
- [ ] (Optional) Nastavit cronjob pro měsíční backup
- [ ] Dokumentovat heslo v recovery docs

## 🆘 Emergency Contacts

**Při ztrátě přístupu:**
1. Proton Drive web UI: https://drive.proton.me
2. HAS server: `ssh root@192.168.0.58 -p 2222`
3. Recovery keys na fyzickém USB (pokud existuje)

---

*Last updated: 2025-11-18*
*Verze: 1.0*
