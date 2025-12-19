# Tailscale SSH Configuration - November 2025

**Status:** ✅ PRODUCTION - Deployed with GOMAXPROCS workarounds
**Date:** 2025-11-11

---

## Overview

Tailscale SSH provides encrypted SSH access over the Tailscale VPN network, with built-in authentication through Tailscale accounts. This supplements the standard SSH configuration.

### Current Status

| Server | Tailscale IP | RunSSH | GOMAXPROCS | Status |
|--------|--------------|--------|------------|--------|
| **Aspire-PC** | 100.100.76.117 | ✅ true | 2 | ⚠️ Incoming connections fail |
| **HAS** | 100.79.142.112 | ✅ true | 2 | ✅ Fully functional |
| **LLMS** | 100.126.243.56 | ✅ true | 4 | ✅ Fully functional |
| **minipc** | 100.96.53.47 | ✅ true | 1 | ✅ Fully functional |

---

## Critical: GOMAXPROCS Configuration

### The Problem

Tailscale binaries built with Go 1.25.3 crash on older CPUs without proper GOMAXPROCS setting:

```bash
$ tailscale version
fatal error: procresize: invalid arg

runtime stack:
runtime.throw({0xdfa651?, 0x0?})
    runtime/panic.go:1094 +0x48
runtime.procresize(0x0?)
    runtime/proc.go:5872 +0x9b6
```

### The Solution

**Always set GOMAXPROCS before calling tailscale commands:**

```bash
GOMAXPROCS=2 tailscale status
GOMAXPROCS=2 tailscale up --ssh
```

### Server-Specific GOMAXPROCS Values

| Server | CPU | Cores | GOMAXPROCS |
|--------|-----|-------|------------|
| Aspire-PC | Intel E8400 | 2 | 2 |
| HAS | AMD E-300 | 2 | 2 |
| LLMS | Intel Q9550 | 4 | 4 |
| minipc | Intel Atom N280 | 1 (+ HT) | **1** |

**Important:** Atom N280 has 1 physical core + HyperThreading. Use GOMAXPROCS=1, NOT 2!

---

## Installation

### Tailscale Installation (Debian/Ubuntu)

```bash
# Add Tailscale repository
curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/jammy.noarmor.gpg | sudo tee /usr/share/keyrings/tailscale-archive-keyring.gpg >/dev/null
curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/jammy.tailscale-package-archive.list | sudo tee /etc/apt/sources.list.d/tailscale.list

# Install
sudo apt update
sudo apt install tailscale

# Verify
tailscale version
```

### Tailscale Installation (Alpine Linux)

```bash
# Install from Alpine repositories
apk add tailscale

# Or download latest stable manually (for newer version)
cd /tmp
wget https://pkgs.tailscale.com/stable/tailscale_1.90.6_amd64.tgz
tar xzf tailscale_1.90.6_amd64.tgz
sudo cp tailscale_1.90.6_amd64/tailscale* /usr/local/bin/
```

---

## Configuration

### Environment File (/etc/default/tailscaled)

**For systemd systems:**

```bash
# /etc/default/tailscaled
PORT="41641"
FLAGS=""
GOMAXPROCS=2  # Adjust based on CPU
```

### Init Script (SysVinit/OpenRC)

**For /etc/init.d/tailscaled:**

```bash
#!/bin/sh
DAEMON=/usr/sbin/tailscaled
PIDFILE=/var/run/tailscaled.pid
DAEMON_ARGS="--state=/var/lib/tailscale/tailscaled.state --socket=/run/tailscale/tailscaled.sock"

# Fix for Go runtime on dual-core CPU
export GOMAXPROCS=2

# ... rest of init script
```

**For Alpine OpenRC (/etc/conf.d/tailscale):**

```bash
# /etc/conf.d/tailscale
PORT="41641"
TAILSCALED_OPTS=""

# Fix for Go runtime on AMD E-300 (2 cores)
export GOMAXPROCS=2
```

---

## Enabling Tailscale SSH

### Initial Setup

```bash
# Start tailscaled daemon
sudo systemctl start tailscaled
# or
sudo /etc/init.d/tailscaled start

# Authenticate and enable SSH
sudo GOMAXPROCS=2 tailscale up --ssh --accept-routes

# This will open a browser for authentication
# After auth, SSH is automatically enabled
```

### Enable SSH on Existing Connection

```bash
# If already connected to Tailscale, just enable SSH
sudo GOMAXPROCS=2 tailscale set --ssh=true

# Verify
GOMAXPROCS=2 tailscale debug prefs | grep RunSSH
# Should show: "RunSSH": true,
```

### Set Operator (Non-root Access)

```bash
# Allow regular user to control Tailscale
sudo GOMAXPROCS=2 tailscale set --operator=$USER

# Now can use without sudo
GOMAXPROCS=2 tailscale status
```

---

## Using Tailscale SSH

### Basic Connection

```bash
# Connect via Tailscale hostname
GOMAXPROCS=2 tailscale ssh user@hostname

# Examples
GOMAXPROCS=2 tailscale ssh root@has-server
GOMAXPROCS=2 tailscale ssh milhy777@llm-server
GOMAXPROCS=2 tailscale ssh milhy777@minipc
```

### Connection via IP

```bash
GOMAXPROCS=2 tailscale ssh user@100.79.142.112
```

### Testing Connectivity

```bash
# Ping test
GOMAXPROCS=2 tailscale ping has-server

# Status check
GOMAXPROCS=2 tailscale status
```

---

## Wrapper Scripts

### System-wide Wrapper

To avoid typing GOMAXPROCS every time, create a wrapper:

```bash
# /usr/local/bin/tailscale-wrapper
#!/bin/bash
export GOMAXPROCS=2
exec /usr/bin/tailscale "$@"
```

Make executable and use:
```bash
chmod +x /usr/local/bin/tailscale-wrapper
tailscale-wrapper status
```

### Shell Alias

Add to `~/.zshrc` or `~/.bashrc`:

```bash
alias tailscale='GOMAXPROCS=2 /usr/bin/tailscale'
```

**Note:** Aliases don't work with `sudo`, use wrapper script for system commands.

---

## Troubleshooting

### Issue: Tailscale SSH Timeout (Aspire-PC)

**Symptom:**
```bash
$ tailscale ssh aspire-pc
Dial("aspire-pc.tailb42db0.ts.net.", 22): unexpected HTTP response: 502 Bad Gateway
```

**Cause:** Tailscale SSH server not listening on Aspire (known issue)

**Workaround:** Use standard SSH:
```bash
ssh -p 22 milhy777@192.168.0.10  # Local network
ssh -p 22 milhy777@100.100.76.117  # Won't work until fixed
```

### Issue: "procresize: invalid arg"

**Solution:** Always use GOMAXPROCS:
```bash
GOMAXPROCS=2 tailscale COMMAND
```

### Issue: Authentication Required

**Symptom:**
```
# Tailscale SSH requires an additional check.
# To authenticate, visit: https://login.tailscale.com/a/XXXXX
```

**Solution:** Visit the URL in browser, approve the connection.

### Issue: "bad tailscale-authstate2 cookie"

**Cause:** Old authentication session

**Solution:**
```bash
# Logout and re-authenticate
sudo GOMAXPROCS=2 tailscale logout
sudo GOMAXPROCS=2 tailscale up --ssh --accept-routes
```

---

## Firewall Configuration

Tailscale uses UDP port 41641 by default:

```bash
# UFW
sudo ufw allow 41641/udp comment 'Tailscale'

# iptables
sudo iptables -A INPUT -p udp --dport 41641 -j ACCEPT
```

---

## Advantages Over Standard SSH

✅ **Built-in VPN encryption** - All traffic encrypted end-to-end
✅ **NAT traversal** - Works behind firewalls without port forwarding
✅ **Centralized authentication** - Managed through Tailscale account
✅ **Automatic IP assignment** - Stable IPs even on dynamic networks
✅ **Zero-config** - No SSH key distribution needed

---

## Limitations

⚠️ **Requires internet** - Tailscale coordination server needed for discovery
⚠️ **Account dependency** - Tied to Tailscale account
⚠️ **GOMAXPROCS workaround** - Extra complexity on older CPUs
⚠️ **Aspire incoming issue** - Aspire can't receive Tailscale SSH connections

---

## Current Network Topology

```
Tailscale Network (100.x.x.x/8)
├── Aspire-PC: 100.100.76.117 ──> [Can SSH to others]
├── HAS: 100.79.142.112 ──> [Fully functional]
├── LLMS: 100.126.243.56 ──> [Fully functional]
└── minipc: 100.96.53.47 ──> [Fully functional]

Local Network (192.168.0.x/24)
├── Aspire-PC: 192.168.0.10:22
├── HAS: 192.168.0.58:2222
├── LLMS: 192.168.0.41:2222
└── minipc: 192.168.0.111:2222
```

**Recommendation:** Use standard SSH for reliability, Tailscale SSH as backup/remote access.

---

## Related Documentation

- [SSH Unified Configuration](./ssh-unified-2025.md) - Standard SSH setup
- [Network Topology](./network-topology.md) - Full ecosystem map

---

**Document Version:** 1.0
**Last Updated:** 2025-11-11
**Status:** Production with Known Limitations
