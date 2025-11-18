# tmux Auto-start Deployment Instructions

**Created:** 2025-11-11
**Session:** SSH Unification Session

---

## Deployment Status

| Server | Status | Shell | Notes |
|--------|--------|-------|-------|
| **Aspire-PC** | ✅ Deployed | ZSH | Completed 2025-11-11 23:19 |
| **LLMS** | ✅ Deployed | Bash | Completed 2025-11-11 23:20 |
| **HAS** | ⏳ Pending | ZSH | Server offline during deployment |
| **minipc** | ℹ️ Already has it | Unknown | Needs documentation of existing setup |

---

## For HAS (Alpine Linux, ZSH)

**When HAS comes back online:**

### Step 1: Backup Current Configuration
```bash
ssh root@HAS "cp ~/.zshrc ~/.zshrc.backup.\$(date +%Y%m%d_%H%M%S)"
```

### Step 2: Add tmux Auto-attach
```bash
cat << 'EOF' | ssh root@HAS "cat >> ~/.zshrc"

# ============================================================================
# tmux Auto-attach for SSH Sessions
# ============================================================================

if [[ -n "$SSH_CONNECTION" ]] && [[ -z "$TMUX" ]] && [[ $- == *i* ]]; then
    if ! command -v /usr/bin/tmux &> /dev/null; then
        echo "⚠️  tmux is not installed. Install with: apk add tmux"
        return
    fi

    echo "🔌 SSH session detected - tmux auto-attach"
    echo ""

    SESSIONS=$(/usr/bin/tmux list-sessions 2>/dev/null)

    if [[ -n "$SESSIONS" ]]; then
        echo "📋 Available tmux sessions:"
        /usr/bin/tmux list-sessions | nl -w2 -s'. '
        echo ""
        echo "Choose session [1-N] or press Enter for new session:"
        read -r -t 10 SESSION_NUM

        if [[ -n "$SESSION_NUM" ]] && [[ "$SESSION_NUM" =~ ^[0-9]+$ ]]; then
            SESSION_NAME=$(/usr/bin/tmux list-sessions -F '#{session_name}' | sed -n "${SESSION_NUM}p")

            if [[ -n "$SESSION_NAME" ]]; then
                echo "Attaching to session: $SESSION_NAME"
                /usr/bin/tmux attach-session -t "$SESSION_NAME"
            else
                echo "Invalid session number, creating new session..."
                /usr/bin/tmux new-session -s "ssh-$(date +%Y%m%d-%H%M%S)"
            fi
        else
            echo "Creating new session..."
            /usr/bin/tmux new-session -s "ssh-$(date +%Y%m%d-%H%M%S)"
        fi
    else
        echo "📋 No existing sessions, creating default session..."
        /usr/bin/tmux new-session -s "main"
    fi
fi
EOF
```

### Step 3: Verify Syntax
```bash
ssh root@HAS "zsh -n ~/.zshrc && echo '✅ HAS Syntax OK' || echo '❌ HAS Syntax error'"
```

### Step 4: Test SSH Connection
```bash
ssh root@HAS
# Should see tmux auto-attach prompt
```

---

## For minipc (Already Implemented)

**minipc already has tmux auto-start working.** This was mentioned in the original request: "jestli si vzopominas tak na 'ssh minipc' se automaticky spousti tmux a pta se te kam se chces pripojit"

**When minipc comes back online, document the existing setup:**

### Step 1: Identify Shell
```bash
ssh milhy777@minipc "echo \$SHELL"
```

### Step 2: Read Existing Configuration
```bash
# If ZSH:
ssh milhy777@minipc "cat ~/.zshrc | grep -A20 tmux"

# If Bash:
ssh milhy777@minipc "cat ~/.bashrc | grep -A20 tmux"
```

### Step 3: Document in Project
Create documentation of minipc's existing tmux auto-start implementation for reference and consistency with other servers.

---

## Verification Checklist

After deployment to HAS, verify all servers:

### From Aspire-PC:
```bash
# Test SSH to each server - should see tmux prompt
ssh root@HAS        # Should show tmux auto-attach
ssh milhy777@LLMS   # Should show tmux auto-attach
ssh milhy777@minipc # Should show tmux auto-attach (existing)
```

### Verify tmux Functionality:
```bash
# On each server after connecting:
echo $TMUX  # Should show tmux socket path
tmux list-sessions  # Should show current session
# Try Ctrl+b d to detach
# Reconnect and see session is still running
```

---

## Rollback Procedures

### Aspire-PC Rollback
```bash
cp ~/.zshrc.backup.20251111_231900 ~/.zshrc
source ~/.zshrc
```

### LLMS Rollback
```bash
ssh LLMS "cp ~/.bashrc.backup.YYYYMMDD_HHMMSS ~/.bashrc"
```

### HAS Rollback (when deployed)
```bash
ssh root@HAS "cp ~/.zshrc.backup.YYYYMMDD_HHMMSS ~/.zshrc"
```

---

## Known Issues

### Issue: tmux Plugin Conflict on Aspire
**Symptom:**
```
_zsh_tmux_plugin_run: příkaz nebyl nalezen
alias tmux=_zsh_tmux_plugin_run
```

**Cause:** Oh My Zsh tmux plugin creates alias that conflicts with direct binary call

**Solution:** Use `/usr/bin/tmux` instead of `tmux` in auto-attach script (already implemented)

---

## Network Issues During Deployment

**HAS and minipc were offline** during the deployment session due to network connectivity issues:

```bash
$ ping 192.168.0.58
PING 192.168.0.58 (192.168.0.58) 56(84) bytes of data.
From 192.168.0.41 icmp_seq=1 Destination Host Unreachable
--- 192.168.0.58 ping statistics ---
2 packets transmitted, 0 received, +2 errors, 100% packet loss

$ ssh minipc
ssh: connect to host 192.168.0.111 port 2222: Connection timed out
```

**Impact:** Could not complete deployment to HAS or verify minipc's existing setup. These must be completed when servers are back online.

---

## Related Documentation

- [tmux Auto-start Guide](./tmux-autostart-2025.md) - Complete tmux configuration guide
- [SSH Unified Configuration](./ssh-unified-2025.md) - SSH setup
- [CHANGELOG-2025-11-11](../CHANGELOG-2025-11-11.md) - Session summary

---

**Document Version:** 1.0
**Last Updated:** 2025-11-11 23:22
**Status:** Partial Deployment (2/4 servers completed)
