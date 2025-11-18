# SSH Unified Configuration - November 2025

**Status:** ✅ PRODUCTION - Successfully unified across all ecosystem servers
**Date:** 2025-11-11
**Implemented by:** Claude Code + User collaborative session

---

## Overview

This document describes the **successfully unified SSH configuration** implemented across the ecosystem. This represents the resolution of the "SSH Hell" described in the project chronicles.

### Ecosystem Servers

| Server | Hostname | IP Address | SSH Port | CPU | GOMAXPROCS |
|--------|----------|------------|----------|-----|------------|
| **Aspire-PC** | Aspire-PC | 192.168.0.10 | 22 (default) | Intel E8400 (2 cores) | 2 |
| **HAS** | home-automat-server | 192.168.0.58 | 2222 | AMD E-300 (2 cores) | 2 |
| **LLMS** | LLMS | 192.168.0.41 | 2222 | Intel Q9550 (4 cores) | 4 |
| **minipc** | MiniPC | 192.168.0.111 | 2222 | Intel Atom N280 (1 core + HT) | 1 |

---

## Unified SSH Server Configuration

### Standard sshd_config (HAS, LLMS, minipc)

**Location:** `/etc/ssh/sshd_config`

```sshd_config
# Unified SSH Configuration
# Based on ecosystem standard with server-specific adjustments

# Network
Port 2222
AddressFamily inet
ListenAddress 0.0.0.0

# Authentication
PermitRootLogin no                    # minipc/LLMS
PermitRootLogin prohibit-password     # HAS only
PubkeyAuthentication yes
PasswordAuthentication no
PermitEmptyPasswords no
ChallengeResponseAuthentication no
MaxAuthTries 3
LoginGraceTime 30

# Protocol & Keys
Protocol 2
HostKey /etc/ssh/ssh_host_rsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key
HostKey /etc/ssh/ssh_host_ed25519_key

# Cryptography (hardened)
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr
MACs hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,hmac-sha2-256,hmac-sha2-512
KexAlgorithms curve25519-sha256@libssh.org,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512

# Session Management
MaxSessions 2
ClientAliveInterval 300
ClientAliveCountMax 2

# Access Control
AllowUsers milhy777          # Standard user
# AllowUsers root            # HAS only
DenyUsers guest

# Features
X11Forwarding yes            # Required for remote desktop
AllowTcpForwarding yes
AllowAgentForwarding yes
PermitTunnel yes
GatewayPorts no

# Logging
SyslogFacility AUTH
LogLevel VERBOSE

# Misc
UsePAM yes
PrintMotd no
AcceptEnv LANG LC_*
Subsystem sftp /usr/lib/openssh/sftp-server
```

### Aspire-PC Configuration (Default Port)

**Location:** `/etc/ssh/sshd_config`

```sshd_config
Include /etc/ssh/sshd_config.d/*.conf
KbdInteractiveAuthentication no
UsePAM yes
X11Forwarding yes
PrintMotd no
AcceptEnv LANG LC_*
Subsystem sftp /usr/lib/openssh/sftp-server
```

**Note:** Aspire uses default port 22 as workstation. All servers connect TO Aspire, but Aspire doesn't need hardened config as it's behind local network.

---

## Unified SSH Client Configuration

### Standard ~/.ssh/config

**Location:** `~/.ssh/config` (on all servers)

```ssh_config
# Unified Ecosystem SSH Client Configuration

Host HAS
    HostName 192.168.0.58
    User root
    IdentityFile ~/.ssh/unified_ecosystem_key
    Port 2222
    StrictHostKeyChecking no
    PasswordAuthentication no

Host LLMS
    HostName 192.168.0.41
    User milhy777
    IdentityFile ~/.ssh/unified_ecosystem_key
    Port 2222
    StrictHostKeyChecking no
    PasswordAuthentication no

Host Aspire
    HostName 192.168.0.10
    User milhy777
    IdentityFile ~/.ssh/unified_ecosystem_key
    Port 22
    StrictHostKeyChecking no
    PasswordAuthentication no

Host minipc
    HostName 192.168.0.111
    User milhy777
    IdentityFile ~/.ssh/unified_ecosystem_key
    Port 2222
    StrictHostKeyChecking no
    PasswordAuthentication no
```

**Key Features:**
- Unified key (`unified_ecosystem_key`) for all connections
- Hostname aliases for easy access
- Disabled strict host checking (trusted local network)
- Password authentication disabled (key-only)

---

## SSH Keys

### Key Generation

**Primary key:** `~/.ssh/unified_ecosystem_key`

```bash
# Generate unified ecosystem key (Ed25519 recommended)
ssh-keygen -t ed25519 -f ~/.ssh/unified_ecosystem_key -C "ecosystem@unified"

# Or RSA for older systems
ssh-keygen -t rsa -b 4096 -f ~/.ssh/unified_ecosystem_key -C "ecosystem@unified"
```

### Key Distribution

```bash
# Copy to all servers
ssh-copy-id -i ~/.ssh/unified_ecosystem_key.pub user@server -p PORT

# Manual distribution (if ssh-copy-id unavailable)
cat ~/.ssh/unified_ecosystem_key.pub | ssh user@server -p PORT "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

### Permission Requirements

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/unified_ecosystem_key
chmod 644 ~/.ssh/unified_ecosystem_key.pub
chmod 600 ~/.ssh/authorized_keys
```

---

## Firewall Configuration

### UFW Rules (Debian-based systems)

```bash
# Allow SSH on unified port
sudo ufw allow 2222/tcp comment 'SSH unified port'

# Remove default port 22 (if migrated)
sudo ufw delete allow 22/tcp

# Check status
sudo ufw status numbered
```

### iptables (Alpine/minimal systems)

```bash
# Allow SSH port
iptables -A INPUT -p tcp --dport 2222 -j ACCEPT

# Save rules
/etc/init.d/iptables save
```

---

## Testing & Verification

### Connection Test Matrix

```bash
# Test from Aspire to all servers
for server in HAS LLMS minipc; do
    echo "Testing $server..."
    ssh $server "hostname && echo 'SSH OK'"
done

# Test from HAS to all servers
ssh HAS "for s in Aspire LLMS minipc; do echo Testing \$s; ssh \$s hostname; done"
```

### Expected Results

✅ All connections should work without password prompts
✅ No "Permission denied" errors
✅ No "Connection refused" on correct ports
✅ Hostname resolution working via ~/.ssh/config

---

## Troubleshooting

### Common Issues

**1. Connection Refused**
```bash
# Check SSH service is running
sudo systemctl status sshd
# or
sudo service ssh status

# Check listening ports
ss -tlnp | grep sshd
netstat -tlnp | grep sshd
```

**2. Permission Denied (publickey)**
```bash
# Verify key permissions
ls -la ~/.ssh/

# Check authorized_keys on target server
ssh user@server -p PORT "cat ~/.ssh/authorized_keys"

# Test with verbose output
ssh -vvv user@server -p PORT
```

**3. Port 22 vs 2222 Confusion**
- **Aspire:** Port 22 (default)
- **All others:** Port 2222
- Always check `~/.ssh/config` for correct port

---

## Implementation Notes

### Init Script Configuration (SysVinit/OpenRC systems)

**For systems using init.d:**
```bash
# Edit /etc/init.d/tailscaled (example with GOMAXPROCS)
export GOMAXPROCS=2
DAEMON_ARGS="--state=/var/lib/tailscale/tailscaled.state --socket=/run/tailscale/tailscaled.sock"
```

### Systemd Configuration

**For systems using systemd:**
```bash
# Edit /etc/default/tailscaled
PORT="41641"
FLAGS=""
GOMAXPROCS=2  # Adjust based on CPU cores
```

---

## Security Considerations

### Strengths
✅ Password authentication disabled
✅ Strong cryptographic algorithms (ChaCha20, AES-GCM, Curve25519)
✅ Limited authentication attempts (MaxAuthTries 3)
✅ Short login grace period (30s)
✅ Verbose logging for audit trail
✅ User whitelisting (AllowUsers)

### Recommendations
- Regularly rotate SSH keys (every 6-12 months)
- Monitor `/var/log/auth.log` for unauthorized attempts
- Consider fail2ban for additional protection
- Use Tailscale SSH as backup access method

---

## Migration from Previous Configuration

### Changes Made (2025-11-11)

**minipc:**
- Port: 22 → 2222
- PasswordAuthentication: yes → no
- Added hardened ciphers/MACs/KEX
- Added MaxAuthTries, LoginGraceTime
- Added AllowUsers whitelist

**HAS:**
- Already on port 2222 ✓
- Updated to unified key
- Hardened configuration maintained

**LLMS:**
- Already on port 2222 ✓
- Updated to unified key

**Aspire:**
- Kept default port 22 (workstation)
- Updated client config only

### Rollback Procedure

All original configs backed up as:
```
/etc/ssh/sshd_config.backup.YYYYMMDD_HHMMSS
```

To rollback:
```bash
sudo cp /etc/ssh/sshd_config.backup.YYYYMMDD_HHMMSS /etc/ssh/sshd_config
sudo systemctl restart sshd
```

---

## Related Documentation

- [SSH Hell Chronicle](../stories/ssh-hell-chronicle-en.md) - The problems that led to this solution
- [Tailscale SSH Configuration](./tailscale-ssh-2025.md) - Tailscale-based SSH access
- [tmux Integration](./tmux-configuration.md) - Automated tmux sessions for SSH
- [Network Topology](./network-topology.md) - Full ecosystem network map

---

**Document Version:** 1.0
**Last Updated:** 2025-11-11
**Status:** Production - Successfully Deployed
