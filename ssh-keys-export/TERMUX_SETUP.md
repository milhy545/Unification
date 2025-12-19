# SSH Setup pro Termux (Android Mobile/Tablet)

## 1. Instalace Termux a potřebných balíčků

```bash
# V Termuxu na mobilu/tabletu:
pkg update && pkg upgrade
pkg install openssh
```

## 2. Import SSH klíče

### Metoda A: Přes USB/SD kartu
1. Zkopíruj `unified_ecosystem_key` na mobil/tablet (USB kabel nebo SD karta)
2. V Termuxu:
```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
cp /storage/emulated/0/Download/unified_ecosystem_key ~/.ssh/
chmod 600 ~/.ssh/unified_ecosystem_key
```

### Metoda B: Přes Termux API (pokud máš Termux:API)
```bash
termux-storage-get ~/unified_ecosystem_key
mkdir -p ~/.ssh
mv ~/unified_ecosystem_key ~/.ssh/
chmod 600 ~/.ssh/unified_ecosystem_key
```

### Metoda C: Přes cloud (OneDrive, Google Drive, atd.)
1. Nahraj `unified_ecosystem_key` do cloudu z PC
2. Stáhni ho v mobilu
3. Zkopíruj do Termux (jako Metoda A)

## 3. Vytvoř SSH config v Termuxu

```bash
cat > ~/.ssh/config << 'EOF'
# Aspire Workstation
Host Aspire
    HostName 192.168.0.10
    User milhy777
    IdentityFile ~/.ssh/unified_ecosystem_key
    Port 22
    StrictHostKeyChecking no
    PasswordAuthentication no

# LLMS Server
Host LLMS
    HostName 192.168.0.41
    User milhy777
    IdentityFile ~/.ssh/unified_ecosystem_key
    Port 2222
    StrictHostKeyChecking no
    PasswordAuthentication no

# Home Automation Server
Host HAS
    HostName 192.168.0.58
    User root
    IdentityFile ~/.ssh/unified_ecosystem_key
    Port 2222
    StrictHostKeyChecking no
    PasswordAuthentication no

# minipc
Host minipc
    HostName 192.168.0.80
    User milhy777
    IdentityFile ~/.ssh/unified_ecosystem_key
    Port 2222
    StrictHostKeyChecking no
    PasswordAuthentication no

# Tailscale přístup (když nejsi doma)
Host HAS-tailscale
    HostName 100.90.137.86
    User root
    IdentityFile ~/.ssh/unified_ecosystem_key
    Port 2222
    StrictHostKeyChecking no
    PasswordAuthentication no
EOF

chmod 600 ~/.ssh/config
```

## 4. Test připojení

```bash
# Z lokální sítě:
ssh Aspire
ssh LLMS
ssh HAS
ssh minipc

# Přes Tailscale (když nejsi doma):
# Nejdřív nainstaluj Tailscale na mobil z Google Play
ssh HAS-tailscale
```

## 5. Tmux workflow v Termuxu

Po připojení přes SSH se automaticky spustí `tmux-manager` menu:
- **1** = Připojit k existující session
- **2** = Vytvořit novou session
- **3** = Pokračovat bez tmux

## 6. Bezpečnostní poznámky

⚠️ **DŮLEŽITÉ:**
- Nikdy nesdílej `unified_ecosystem_key` s nikým
- Neskladuj ho v nezabezpečeném cloudu
- Smaž soubor z Download složky po zkopírování do Termuxu
- Ujisti se, že má správná oprávnění (600)

## 7. Troubleshooting

### "Permission denied (publickey)"
```bash
chmod 600 ~/.ssh/unified_ecosystem_key
chmod 700 ~/.ssh
```

### "Connection refused"
- Zkontroluj že jsi ve stejné síti (lokální IP)
- Nebo použij Tailscale variantu

### "No route to host"
- Server může být vypnutý
- Zkontroluj IP adresu pomocí `ping`

## 8. Užitečné Termux aliasy

Přidej do `~/.bashrc` nebo `~/.zshrc` v Termuxu:

```bash
alias ssh-aspire='ssh Aspire'
alias ssh-llms='ssh LLMS'
alias ssh-has='ssh HAS'
alias ssh-minipc='ssh minipc'
alias ssh-has-ts='ssh HAS-tailscale'
```

---

**Vytvořeno:** 2025-11-12
**Unified Ecosystem SSH Key System**
