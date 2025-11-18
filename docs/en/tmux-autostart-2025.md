# tmux Auto-start Configuration - November 2025

**Status:** 🔧 IN PROGRESS - minipc implemented, pending Aspire/HAS/LLMS
**Date:** 2025-11-11

---

## Overview

Automatic tmux session attachment when SSH connections are established. Provides persistent terminal sessions with session management menu.

### Current Status

| Server | tmux Auto-start | Status |
|--------|----------------|--------|
| **minipc** | ✅ Implemented | Fully functional |
| **Aspire-PC** | ❌ Pending | Needs implementation |
| **HAS** | ❌ Pending | Needs implementation |
| **LLMS** | ❌ Pending | Needs implementation |

---

## How It Works

When you SSH into a server with tmux auto-start:

1. **New SSH connection** triggers shell RC file (.zshrc or .bashrc)
2. **Script checks** if already inside tmux (prevents nested sessions)
3. **Lists available** tmux sessions or creates default session
4. **Prompts user** to select session or create new one
5. **Attaches to** selected session

---

## Implementation

### minipc Configuration (Reference)

**Note:** minipc is currently offline, this is reconstructed from session memory.

```bash
# In ~/.zshrc or ~/.bashrc
# tmux auto-attach for SSH sessions

if [[ -n "$SSH_CONNECTION" ]] && [[ -z "$TMUX" ]] && [[ $- == *i* ]]; then
    # Check if tmux is available
    if command -v tmux &> /dev/null; then
        # Get existing sessions
        SESSIONS=$(tmux list-sessions 2>/dev/null)

        if [[ -n "$SESSIONS" ]]; then
            echo "Available tmux sessions:"
            tmux list-sessions
            echo ""
            echo "Select session number (or press Enter for new session):"
            read -r SESSION_CHOICE

            if [[ -n "$SESSION_CHOICE" ]]; then
                # Attach to specific session
                tmux attach-session -t "$SESSION_CHOICE" 2>/dev/null || tmux new-session
            else
                # Create new session
                tmux new-session
            fi
        else
            # No sessions exist, create default
            echo "No tmux sessions found, creating new session..."
            tmux new-session -s "ssh-$(date +%s)"
        fi
    fi
fi
```

### Standard Configuration Template

**Location:** Add to `~/.zshrc` (Oh My Zsh) or `~/.bashrc`

```bash
# ============================================================================
# tmux Auto-attach for SSH Sessions
# ============================================================================

# Only run for SSH connections, not already in tmux, and interactive shells
if [[ -n "$SSH_CONNECTION" ]] && [[ -z "$TMUX" ]] && [[ $- == *i* ]]; then
    # Ensure tmux is installed
    if ! command -v tmux &> /dev/null; then
        echo "⚠️  tmux is not installed. Install with: sudo apt install tmux"
        return
    fi

    echo "🔌 SSH session detected - tmux auto-attach"
    echo ""

    # List existing sessions
    SESSIONS=$(tmux list-sessions 2>/dev/null)

    if [[ -n "$SESSIONS" ]]; then
        echo "📋 Available tmux sessions:"
        tmux list-sessions | nl -w2 -s'. '
        echo ""
        echo "Choose session [1-N] or press Enter for new session:"
        read -r -t 10 SESSION_NUM

        if [[ -n "$SESSION_NUM" ]] && [[ "$SESSION_NUM" =~ ^[0-9]+$ ]]; then
            # Get session name by line number
            SESSION_NAME=$(tmux list-sessions -F '#{session_name}' | sed -n "${SESSION_NUM}p")

            if [[ -n "$SESSION_NAME" ]]; then
                echo "Attaching to session: $SESSION_NAME"
                tmux attach-session -t "$SESSION_NAME"
            else
                echo "Invalid session number, creating new session..."
                tmux new-session -s "ssh-$(date +%Y%m%d-%H%M%S)"
            fi
        else
            echo "Creating new session..."
            tmux new-session -s "ssh-$(date +%Y%m%d-%H%M%S)"
        fi
    else
        echo "📋 No existing sessions, creating default session..."
        tmux new-session -s "main"
    fi
fi
```

---

## Deployment Instructions

### Prerequisites

```bash
# Install tmux if not present
sudo apt install tmux -y

# Verify installation
tmux -V
```

### For ZSH (Oh My Zsh) - Aspire, HAS, LLMS

```bash
# Backup current .zshrc
cp ~/.zshrc ~/.zshrc.backup.$(date +%Y%m%d_%H%M%S)

# Add tmux auto-attach to end of .zshrc
cat >> ~/.zshrc << 'EOF'

# ============================================================================
# tmux Auto-attach for SSH Sessions
# ============================================================================

if [[ -n "$SSH_CONNECTION" ]] && [[ -z "$TMUX" ]] && [[ $- == *i* ]]; then
    if ! command -v tmux &> /dev/null; then
        echo "⚠️  tmux is not installed. Install with: sudo apt install tmux"
        return
    fi

    echo "🔌 SSH session detected - tmux auto-attach"
    echo ""

    SESSIONS=$(tmux list-sessions 2>/dev/null)

    if [[ -n "$SESSIONS" ]]; then
        echo "📋 Available tmux sessions:"
        tmux list-sessions | nl -w2 -s'. '
        echo ""
        echo "Choose session [1-N] or press Enter for new session:"
        read -r -t 10 SESSION_NUM

        if [[ -n "$SESSION_NUM" ]] && [[ "$SESSION_NUM" =~ ^[0-9]+$ ]]; then
            SESSION_NAME=$(tmux list-sessions -F '#{session_name}' | sed -n "${SESSION_NUM}p")

            if [[ -n "$SESSION_NAME" ]]; then
                echo "Attaching to session: $SESSION_NAME"
                tmux attach-session -t "$SESSION_NAME"
            else
                echo "Invalid session number, creating new session..."
                tmux new-session -s "ssh-$(date +%Y%m%d-%H%M%S)"
            fi
        else
            echo "Creating new session..."
            tmux new-session -s "ssh-$(date +%Y%m%d-%H%M%S)"
        fi
    else
        echo "📋 No existing sessions, creating default session..."
        tmux new-session -s "main"
    fi
fi
EOF

# Reload shell configuration
source ~/.zshrc
```

### For Bash (if needed)

```bash
# Same process but edit ~/.bashrc instead
cp ~/.bashrc ~/.bashrc.backup.$(date +%Y%m%d_%H%M%S)
# ... add same code to ~/.bashrc
source ~/.bashrc
```

---

## Testing

### Test tmux Auto-attach

```bash
# From another server, SSH in
ssh user@target-server

# Should see:
# 🔌 SSH session detected - tmux auto-attach
# 📋 Available tmux sessions:
#  1. main: 1 windows (created Mon Nov 11 23:00:00 2025)
#  2. work: 3 windows (created Mon Nov 11 22:00:00 2025)
#
# Choose session [1-N] or press Enter for new session:
```

### Verify tmux is Running

```bash
# Inside the SSH session
echo $TMUX
# Should output something like: /tmp/tmux-1000/default,12345,0
```

### Manual tmux Commands

```bash
# Detach from session (keep it running)
Ctrl+b d

# List sessions
tmux list-sessions

# Attach to specific session
tmux attach-session -t session-name

# Create new named session
tmux new-session -s work

# Kill session
tmux kill-session -t session-name
```

---

## tmux Basic Keybindings

**Prefix key:** `Ctrl+b` (press before any command)

| Keybinding | Action |
|------------|--------|
| `Ctrl+b d` | Detach from session |
| `Ctrl+b c` | Create new window |
| `Ctrl+b n` | Next window |
| `Ctrl+b p` | Previous window |
| `Ctrl+b 0-9` | Switch to window N |
| `Ctrl+b %` | Split window vertically |
| `Ctrl+b "` | Split window horizontally |
| `Ctrl+b o` | Switch pane |
| `Ctrl+b x` | Kill current pane |
| `Ctrl+b [` | Enter copy mode (scroll) |
| `Ctrl+b ?` | List all keybindings |

---

## Configuration Customization

### Custom tmux.conf

Create `~/.tmux.conf` for enhanced experience:

```bash
# ~/.tmux.conf - Enhanced tmux configuration

# Enable mouse support
set -g mouse on

# Increase scrollback buffer
set -g history-limit 10000

# Start windows and panes at 1, not 0
set -g base-index 1
setw -g pane-base-index 1

# Better split commands
bind | split-window -h
bind - split-window -v

# Reload config
bind r source-file ~/.tmux.conf \; display "Config reloaded!"

# Status bar customization
set -g status-style bg=colour235,fg=colour136
set -g status-left '[#S] '
set -g status-right '%H:%M %d-%b-%y'

# Pane border colors
set -g pane-border-style fg=colour238
set -g pane-active-border-style fg=colour51
```

Apply configuration:
```bash
tmux source-file ~/.tmux.conf
```

---

## Troubleshooting

### Issue: "tmux: command not found"

**Solution:**
```bash
sudo apt update
sudo apt install tmux -y
```

### Issue: Nested tmux Sessions

**Symptom:** tmux inside tmux (messy)

**Prevention:** The `[[ -z "$TMUX" ]]` check prevents this

**Fix if it happens:**
```bash
exit  # Exit inner tmux
# Or Ctrl+d to close shell
```

### Issue: Auto-attach Not Working

**Diagnosis:**
```bash
# Check if SSH_CONNECTION is set
echo $SSH_CONNECTION
# Should show: client_ip client_port server_ip server_port

# Check if already in tmux
echo $TMUX
# Should be empty if not in tmux

# Check shell is interactive
echo $-
# Should contain 'i'
```

**Fix:** Verify RC file:
```bash
# For ZSH
cat ~/.zshrc | grep -A20 "tmux Auto-attach"

# For Bash
cat ~/.bashrc | grep -A20 "tmux Auto-attach"
```

### Issue: Session Selection Timeout

**Symptom:** Timeout after 10 seconds, creates new session

**Adjustment:** Change timeout in RC file:
```bash
# Change this line:
read -r -t 10 SESSION_NUM
# To longer timeout (30s):
read -r -t 30 SESSION_NUM
# Or no timeout:
read -r SESSION_NUM
```

---

## Advantages

✅ **Persistent sessions** - Survive network disconnections
✅ **Multiple windows** - Organize work in tabs
✅ **Split panes** - Multiple shells in one view
✅ **Detach/reattach** - Resume exactly where you left off
✅ **Scrollback buffer** - Large history (10000 lines default)
✅ **Copy/paste mode** - Keyboard-driven text selection
✅ **Session sharing** - Multiple SSH connections to same session

---

## Limitations

⚠️ **Learning curve** - Keybindings take time to learn
⚠️ **Ctrl+b prefix** - Extra keypress before commands
⚠️ **Terminal compatibility** - Some terminals have color/rendering issues
⚠️ **Auto-attach on every SSH** - May not want this behavior always

---

## Ecosystem Deployment Plan

### Phase 1: Aspire-PC ✅ (Current Session)
- Install tmux
- Add auto-attach to ~/.zshrc
- Test SSH connection
- Document any issues

### Phase 2: HAS (Alpine Linux)
- Install tmux: `apk add tmux`
- Add auto-attach to ~/.zshrc (Oh My Zsh on HAS)
- Test SSH connection from Aspire
- Verify root user compatibility

### Phase 3: LLMS
- Install tmux: `sudo apt install tmux`
- Add auto-attach to ~/.zshrc
- Test SSH connection from Aspire
- Verify with existing sessions

### Phase 4: Verification
- Test SSH from each server to every other server
- Verify session persistence after network disconnect
- Document final configuration per server

---

## Related Documentation

- [SSH Unified Configuration](./ssh-unified-2025.md) - SSH setup for ecosystem
- [Tailscale SSH Configuration](./tailscale-ssh-2025.md) - VPN SSH access
- [CHANGELOG-2025-11-11](../CHANGELOG-2025-11-11.md) - Session summary

---

**Document Version:** 1.0
**Last Updated:** 2025-11-11
**Status:** Pending Implementation (3/4 servers)
