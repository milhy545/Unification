# SSH Keys Registry - Unification System

> Centrální evidence SSH klíčů a přístupových práv

**Poslední aktualizace**: 2025-12-06 01:45 GMT
**Správce**: Claude Code Agent

---

## Active Production Keys

### unified_ecosystem_key_2025 (PRIMARY)
- **Soubor**: `/home/milhy777/.ssh/unified_ecosystem_key_2025`
- **Type**: ED25519
- **Created**: 2025-11-18
- **Public key**:
  ```
  ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINnS4qZ... unified_ecosystem_key_2025
  ```
- **Fingerprint**: SHA256:... (TODO: doplnit)
- **Status**: ✓ Active
- **Deployed on**:
  - [ ] HAS (192.168.0.58, 100.90.137.86)
  - [ ] LLMS (192.168.0.41, 100.68.65.121)
  - [ ] MiniPC (192.168.0.111, 100.96.53.47)
  - [ ] Workstation (localhost)
- **Purpose**: Unified access pro celý 3 PC Ecosystem

### unified_ecosystem_key (LEGACY - PHASING OUT)
- **Soubor**: `/home/milhy777/.ssh/unified_ecosystem_key`
- **Type**: ED25519
- **Created**: ~2024-09
- **Status**: ⚠️ Deprecated (nahrazeno _2025 verzí)
- **Action**: Archive po úspěšné migraci

---

## Legacy Keys (Archive candidates)

### server_access_key
- **Soubor**: `/home/milhy777/.ssh/server_access_key`
- **Type**: ED25519
- **Created**: 2024-09-28
- **Status**: ⚠️ Legacy
- **Used by**: Starší SSH config pro HAS
- **Action**: Archive po ověření nového klíče

### id_ed25519_server
- **Soubor**: `/home/milhy777/.ssh/id_ed25519_server`
- **Type**: ED25519
- **Created**: 2024-09-28
- **Status**: ⚠️ Legacy
- **Action**: Archive

### id_ed25519_llms
- **Soubor**: `/home/milhy777/.ssh/id_ed25519_llms`
- **Type**: ED25519
- **Created**: 2024-09-28
- **Status**: ⚠️ Legacy
- **Action**: Archive

### id_ed25519
- **Soubor**: `/home/milhy777/.ssh/id_ed25519`
- **Type**: ED25519
- **Created**: 2024-09-28
- **Status**: ⚠️ Legacy
- **Action**: Archive

---

## Mobile/Special Purpose Keys

### id_rsa_phone
- **Soubor**: `/home/milhy777/.ssh/id_rsa_phone`
- **Type**: RSA 3272 bits
- **Created**: 2024-09-28
- **Status**: ⚠️ Old RSA format
- **Purpose**: Phone SSH client (legacy)
- **Action**: Re-generate jako ED25519

### id_rsa_connectbot
- **Soubor**: `/home/milhy777/.ssh/id_rsa_connectbot`
- **Type**: RSA 3381 bits
- **Created**: 2024-09-28
- **Status**: ⚠️ Old RSA format
- **Purpose**: ConnectBot Android app
- **Action**: Re-generate jako ED25519

---

## Service Keys

### github-actions-has
- **Soubor**: `/home/milhy777/.ssh/github-actions-has`
- **Type**: ED25519
- **Created**: 2024-10-12
- **Status**: ✓ Active
- **Purpose**: GitHub Actions deployment na HAS
- **Deployed on**: HAS authorized_keys (deploy user)

### google_compute_engine
- **Soubor**: `/home/milhy777/.ssh/google_compute_engine`
- **Type**: RSA (GCP format)
- **Created**: 2024-11-18
- **Status**: ✓ Active
- **Purpose**: Google Cloud Platform VMs
- **Managed by**: gcloud SDK

---

## Access Matrix

| Key | Workstation | HAS | LLMS | MiniPC | GitHub | GCP |
|-----|-------------|-----|------|--------|--------|-----|
| unified_ecosystem_key_2025 | ⏳ | ⏳ | ⏳ | ⏳ | ❌ | ❌ |
| unified_ecosystem_key | ✓ | ✓ | ✓ | ✓ | ❌ | ❌ |
| github-actions-has | ❌ | ✓ | ❌ | ❌ | ✓ | ❌ |
| google_compute_engine | ❌ | ❌ | ❌ | ❌ | ❌ | ✓ |

**Legend**:
- ✓ = Deployed & Active
- ⏳ = Pending deployment
- ❌ = Not applicable
- ⚠️ = Deprecated/Legacy

---

## Server authorized_keys Status

### HAS (Home-Automation-Server)
- **Path**: `/root/.ssh/authorized_keys`
- **Status**: ⚠️ UNKNOWN (potřeba ověřit přes web terminal)
- **Expected keys**:
  - unified_ecosystem_key_2025 (TODO)
  - github-actions-has (deploy user)

### LLMS
- **Path**: `/home/milhy777/.ssh/authorized_keys`
- **Status**: ❌ OFFLINE (8 days)
- **Expected keys**:
  - unified_ecosystem_key_2025 (TODO)

### MiniPC
- **Path**: `/home/milhy777/.ssh/authorized_keys`
- **Status**: ❌ OFFLINE (24 days, vybitá baterie)
- **Expected keys**:
  - unified_ecosystem_key_2025 (TODO)

### Workstation (Aspire-PC)
- **Path**: `/home/milhy777/.ssh/authorized_keys`
- **Status**: ✓ ONLINE
- **Current**: **EMPTY (0 bytes)** ⚠️
- **Expected keys**:
  - unified_ecosystem_key_2025 (pro localhost access)

---

## Migration Plan

### Fáze 1: Preparation ✓
- [x] Audit existujících klíčů
- [x] Identifikace legacy klíčů
- [x] Vytvoření registru

### Fáze 2: Deployment (PENDING)
- [ ] Fix Tailscale routing (blokuje SSH)
- [ ] Deploy unified_ecosystem_key_2025 na HAS
- [ ] Deploy unified_ecosystem_key_2025 na LLMS (až bude online)
- [ ] Deploy unified_ecosystem_key_2025 na MiniPC (až bude online)
- [ ] Deploy unified_ecosystem_key_2025 na Workstation

### Fáze 3: Validation (PENDING)
- [ ] Test SSH z Workstation → HAS
- [ ] Test SSH z Workstation → LLMS
- [ ] Test SSH z Workstation → MiniPC
- [ ] Test Tailscale SSH přístup
- [ ] Test GitHub Actions deployment

### Fáze 4: Cleanup (PENDING)
- [ ] Archivovat unified_ecosystem_key (starý)
- [ ] Archivovat server_access_key
- [ ] Archivovat id_ed25519_*
- [ ] Archivovat RSA mobile keys
- [ ] Smazat staré klíče z authorized_keys

---

## Security Notes

### Best Practices
- ✓ ED25519 preferred (modernější, bezpečnější než RSA)
- ✓ Separate keys pro production vs. services
- ⚠️ RSA keys deprecated (phone, connectbot)
- ⚠️ authorized_keys prázdný na Workstation

### Known Issues
1. **authorized_keys empty** - Workstation nemá žádné povolené klíče pro příchozí SSH
2. **Legacy RSA keys** - Phone a ConnectBot používají starý RSA formát
3. **Key sprawl** - 11 klíčů celkem, potřeba consolidation
4. **No key rotation policy** - Neexistuje plán rotace klíčů

### Recommendations
1. Implementovat key rotation každých 12 měsíců
2. Re-generate mobile keys jako ED25519
3. Setup centrální SSH CA (optional, pro advanced setup)
4. Pravidelný audit authorized_keys na všech serverech

---

## Useful Commands

```bash
# List all fingerprints
for key in ~/.ssh/*.pub; do
  ssh-keygen -lf "$key"
done

# Copy key to remote server
ssh-copy-id -i ~/.ssh/unified_ecosystem_key_2025.pub user@host

# Verify key on remote
ssh user@host "cat ~/.ssh/authorized_keys"

# Test SSH with specific key
ssh -i ~/.ssh/unified_ecosystem_key_2025 -v user@host

# Generate new ED25519 key
ssh-keygen -t ed25519 -C "comment" -f ~/.ssh/keyname
```

---

**Poznámka**: Tento registr je živý dokument. Aktualizuj po každé změně SSH infrastruktury.
