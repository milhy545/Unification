# minipc Reference Implementation

## 📋 Overview

This directory contains **complete reference implementation** from minipc - the original configuration that served as the template for unified ecosystem setup.

**Source Server:** minipc (192.168.0.80:2222)
**Date Captured:** 2025-11-12
**Purpose:** Reference for all unified configurations across ecosystem

---

## 📁 Directory Structure

```
reference-minipc/
├── README.md                    # This file
├── .bashrc                      # Bash shell configuration
├── .zshrc                       # ZSH shell configuration (primary)
├── .zshrc.antix                 # AntiX-specific ZSH config
├── .zshrc.pre-oh-my-zsh         # Original ZSH before OH MY ZSH
├── .zshrc.workstation           # Alternative workstation config
├── .bash_logout                 # Bash logout script
├── bin/                         # Executable scripts
│   ├── tmux-manager            # ⭐ tmux session manager (REFERENCE)
│   ├── has-status              # HAS server status checker
│   ├── fei-bridge              # FEI bridge wrapper
│   ├── mycoder-ai              # AI coder wrapper
│   └── mycoder-lite            # Lite AI coder wrapper
└── home-scripts/                # Python scripts from home directory
    ├── has-client.sh           # HAS client script
    ├── fei-bridge.py           # FEI bridge Python implementation
    ├── claude-notebook.py      # Claude notebook interface
    ├── mycoder-ai.py           # AI coder main script
    ├── mycoder-claude.py       # Claude-specific coder
    ├── mycoder-fast.py         # Fast AI coder variant
    ├── mycoder-lite.py         # Lite AI coder variant
    ├── mycoder.py              # Base mycoder script
    ├── mycoder-smart.py        # Smart AI coder variant
    ├── mycoder-terminal.py     # Terminal-focused coder
    └── mycoder-ultimate.py     # Ultimate AI coder variant
```

---

## ⭐ Key Configuration Files

### 1. **Shell Configurations**

#### `.bashrc`
- Default Bash shell configuration
- Contains AntiX-specific settings
- Color prompt configuration
- Desktop session aliases (srj, srf, sri, etc.)
- **Important:** Ends with `exec zsh` to switch to ZSH

#### `.zshrc` (PRIMARY)
- Main ZSH configuration with OH MY ZSH
- Theme: `robbyrussell`
- 25 plugins (see below)
- LC_ALL=C.UTF-8 export
- Contains tmux auto-start logic
- AI coder aliases (ai, fast-ai, smart-ai, etc.)

#### `.zshrc.antix`
- AntiX Linux specific ZSH configuration
- Lightweight setup for resource-constrained systems

#### `.zshrc.workstation`
- Alternative configuration for workstation mode
- More feature-rich than standard setup

#### `.zshrc.pre-oh-my-zsh`
- Original ZSH configuration before OH MY ZSH installation
- Useful for rollback reference

---

## 🔌 OH MY ZSH Configuration

### Theme
```zsh
ZSH_THEME="robbyrussell"
```
**Why this theme:**
- Lightweight and fast
- Works on all systems (no Powerline fonts required)
- Clean and readable
- Shows git status

### Plugins (25 total)
```zsh
plugins=(
    git                         # Git integration
    python pip                  # Python development
    sudo                        # Double ESC for sudo
    history                     # Enhanced history
    colored-man-pages           # Colorized man pages
    command-not-found           # Package suggestions
    extract                     # Universal extractor
    copyfile copypath           # Clipboard operations
    dirhistory                  # Directory navigation
    encode64                    # Base64 encoding
    fzf                        # Fuzzy finder
    jsontools                  # JSON utilities
    battery                    # Battery status
    common-aliases             # Useful shortcuts
    history-substring-search   # History search
    magic-enter                # Git status on empty line
    aliases                    # List all aliases
    node npm                   # Node.js development
    tmux                       # tmux integration
    z                          # Smart directory jump
    zsh-autosuggestions        # Fish-like suggestions
    zsh-syntax-highlighting    # Syntax highlighting
)
```

---

## 🎯 tmux Manager (Reference Implementation)

### Location
`bin/tmux-manager`

### Features
- **Interactive menu on SSH login**
- **Smart session detection:**
  - If 1 session exists: auto-attach
  - If multiple sessions: show list with numbers
- **User choices:**
  1. Attach to existing session
  2. Create new session (with custom name)
  3. Skip tmux (regular shell)
- **Clean, readable bash code**
- **User-friendly Czech interface**

### Integration
Called from `.zshrc`:
```zsh
if [[ -z "$TMUX" ]] && [[ "$TERM_PROGRAM" != "vscode" ]]; then
    echo "🚀 Tmux Session Manager"
    ~/bin/tmux-manager
fi
```

**Note:** Not triggered in SSH sessions on minipc, but this is the template for other servers.

---

## 🔧 Utility Scripts

### `bin/has-status`
**Purpose:** Check Home Automation Server status
**Usage:** `has-status`
**Output:** Server availability, services status

### `bin/fei-bridge`
**Purpose:** Wrapper for FEI bridge Python script
**Related:** `home-scripts/fei-bridge.py`

### `bin/mycoder-ai` & `bin/mycoder-lite`
**Purpose:** Wrappers for AI coder Python scripts
**Related:** `home-scripts/mycoder-*.py`

---

## 🐍 Python Scripts

### AI Coder Suite
Multiple variants for different use cases:
- `mycoder.py` - Base implementation
- `mycoder-ai.py` - AI-enhanced version
- `mycoder-claude.py` - Claude API integration
- `mycoder-fast.py` - Fast response variant
- `mycoder-lite.py` - Lightweight variant
- `mycoder-smart.py` - Smart context variant
- `mycoder-terminal.py` - Terminal-optimized
- `mycoder-ultimate.py` - Full-featured variant

### System Integration
- `claude-notebook.py` - Claude notebook interface
- `fei-bridge.py` - FEI system bridge
- `has-client.sh` - HAS client script

---

## 🎯 Unified Configuration Mapping

This reference was used to unify configurations across:

| Server | Status | Config Source |
|--------|--------|---------------|
| **minipc** | ✅ Reference | Original (this) |
| **Aspire** | ✅ Unified | Copied from minipc |
| **HAS** | ✅ Unified | Copied from minipc |
| **LLMS** | ✅ Unified | Copied from minipc |

### What Was Unified
1. **tmux-manager** - Exact copy to all servers
2. **OH MY ZSH theme** - `robbyrussell` everywhere
3. **OH MY ZSH plugins** - 25 plugins identical
4. **Shell behavior** - Consistent UX on SSH login

---

## 📚 Usage as Reference

### For New Server Setup
1. Copy `.zshrc` as template
2. Copy `bin/tmux-manager` to `~/bin/`
3. Install OH MY ZSH: `sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"`
4. Install custom plugins:
   ```bash
   git clone https://github.com/zsh-users/zsh-autosuggestions ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions
   git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting
   ```
5. Adjust `.zshrc` theme and plugins section

### For Configuration Updates
1. Check current minipc config
2. Update this reference if minipc changes
3. Propagate changes to other servers
4. Document in CHANGELOG

---

## 🔄 Maintenance

### When minipc Config Changes
1. Update this reference directory:
   ```bash
   ssh minipc "cat ~/.zshrc" > ~/Develop/Unification/configs/reference-minipc/.zshrc
   ssh minipc "cat ~/bin/tmux-manager" > ~/Develop/Unification/configs/reference-minipc/bin/tmux-manager
   ```
2. Document changes in CHANGELOG
3. Evaluate if other servers need updates

### Version Control
- All files tracked in Unification project
- Git history shows evolution
- Easy rollback if needed

---

## ⚠️ Important Notes

### DO NOT Modify Directly
- These are **reference copies** only
- Modifications should be made on minipc first
- Then captured back to this reference

### Server-Specific Adjustments
Some configs may need adjustments per server:
- Different hardware (CPU, RAM)
- Different services (Docker on HAS, Ollama on LLMS)
- Different user accounts (root on HAS, milhy777 elsewhere)

### Aliases in `.zshrc`
minipc has AI coder aliases:
```zsh
alias ai="python3 ~/mycoder-ai.py"
alias fast-ai="python3 ~/mycoder-fast.py"
alias smart-ai="python3 ~/mycoder-smart.py"
alias terminal-ai="python3 ~/mycoder-terminal.py"
alias claude="python3 ~/claude-notebook.py"
alias mycoder="python3 ~/mycoder-ultimate.py"
alias smart="python3 ~/mycoder-ultimate.py"
alias claude-mycoder="python3 ~/mycoder-claude.py"
```

These reference Python scripts in home directory.
Other servers may not have these scripts installed.

---

## 📊 Configuration Statistics

- **Shell RC files:** 5 (.bashrc, 3x .zshrc variants, .bash_logout)
- **Executable scripts:** 5 (bin/)
- **Python scripts:** 11 (home-scripts/)
- **OH MY ZSH plugins:** 25
- **Lines of config:** ~150 (.zshrc)
- **Lines of code:** ~60 (tmux-manager)

---

## 🎓 Lessons Learned

1. **Simplicity Wins:** robbyrussell theme over complex Powerline themes
2. **Modularity:** Separate scripts in ~/bin/ vs inline code
3. **Consistency:** Same plugins = same experience everywhere
4. **Documentation:** This reference enables reliable replication

---

## 📖 Related Documentation

- [CHANGELOG-2025-11-12-unified-config.md](../../docs/CHANGELOG-2025-11-12-unified-config.md) - Unification process
- [omz-unified-config.zsh](../omz-unified-config.zsh) - OH MY ZSH unified config
- [tmux-manager.sh](../tmux-manager.sh) - tmux manager documentation

---

**Captured:** 2025-11-12
**Maintainer:** Unified Ecosystem Configuration Project
**Status:** ✅ Complete Reference Implementation
