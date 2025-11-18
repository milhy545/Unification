# SSH Keys Export Package

## 📦 Obsah balíčku

- `unified_ecosystem_key` - Privátní SSH klíč (⚠️ CHRAŇ!)
- `unified_ecosystem_key.pub` - Veřejný SSH klíč
- `TERMUX_SETUP.md` - Kompletní návod pro Termux setup

## 🎯 Účel

Tento balíček obsahuje SSH klíče pro přístup ke všem serverům v unified ecosystem:
- Aspire (Workstation) - 192.168.0.10:22
- LLMS (Server) - 192.168.0.41:2222
- HAS (Home Automation Server) - 192.168.0.58:2222
- minipc (Notebook) - 192.168.0.80:2222

## 🔒 Bezpečnost

**KRITICKY DŮLEŽITÉ:**
1. ⚠️ Privátní klíč NIKDY nesdílej s nikým
2. ⚠️ Neskladuj ho na veřejném místě
3. ⚠️ Po přenosu do Termux smaž z Download složky
4. ⚠️ Vždy zkontroluj oprávnění: `chmod 600 unified_ecosystem_key`

## 📱 Pro Termux (Android)

Následuj instrukce v `TERMUX_SETUP.md` - kompletní průvodce instalací.

**Quick start:**
```bash
# 1. Zkopíruj unified_ecosystem_key do mobilu
# 2. V Termuxu:
mkdir -p ~/.ssh
chmod 700 ~/.ssh
cp /storage/emulated/0/Download/unified_ecosystem_key ~/.ssh/
chmod 600 ~/.ssh/unified_ecosystem_key

# 3. Postupuj podle TERMUX_SETUP.md
```

## 🌐 Přístup mimo domácí síť

Pro přístup mimo domácí síť použij **Tailscale VPN**:
1. Nainstaluj Tailscale na mobil/tablet z Google Play
2. Přihlas se stejným účtem jako na PC
3. Použij `ssh HAS-tailscale` (podle TERMUX_SETUP.md)

## 📝 Poznámky

- Všechny servery používají **unified_ecosystem_key** pro autentizaci
- Port 2222 na serverech (HAS, LLMS, minipc)
- Port 22 na Aspire
- tmux-manager menu se spustí automaticky při SSH připojení
- OH MY ZSH je sjednocený na všech serverech (robbyrussell theme)

---

**Verze:** 2025-11-12
**Unified Configuration Project**
