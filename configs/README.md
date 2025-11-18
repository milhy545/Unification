# Unified Configuration Repository

## 📋 Overview

Centralized repository for all unified configurations across the ecosystem. This directory contains reference implementations, deployment scripts, and documentation for consistent system setup.

**Project:** Unified Ecosystem Configuration
**Date Created:** 2025-11-12
**Purpose:** Single source of truth for all system configurations

---

## 📁 Directory Structure

```
configs/
├── README.md                           # This file
├── reference-minipc/                   # ⭐ minipc reference implementation
│   ├── README.md                      # Complete minipc documentation
│   ├── .bashrc                        # Bash configuration
│   ├── .zshrc                         # ZSH configuration (PRIMARY)
│   ├── .zshrc.antix                   # AntiX variant
│   ├── .zshrc.pre-oh-my-zsh          # Pre-OMZ backup
│   ├── .zshrc.workstation            # Workstation variant
│   ├── .bash_logout                   # Logout script
│   ├── bin/                           # Executable scripts
│   │   ├── tmux-manager              # Session manager
│   │   ├── has-status                # HAS checker
│   │   ├── fei-bridge                # FEI wrapper
│   │   ├── mycoder-ai                # AI wrapper
│   │   └── mycoder-lite              # Lite AI wrapper
│   └── home-scripts/                  # Python scripts
│       ├── has-client.sh             # HAS client
│       ├── fei-bridge.py             # FEI bridge
│       ├── claude-notebook.py        # Claude interface
│       └── mycoder-*.py              # AI coder variants (10 files)
├── tmux-manager.sh                    # Documented tmux manager
├── tmux-autostart-menu.sh            # Legacy tmux script (deprecated)
└── omz-unified-config.zsh            # OH MY ZSH unified config
```

---

## 🎯 Key Configuration Files

### 1. **reference-minipc/** ⭐
**Purpose:** Complete reference implementation from minipc
**Status:** PRIMARY SOURCE OF TRUTH
**Contains:** All configs, scripts, and documentation from minipc
**Usage:** Template for new server setup or configuration updates

**Key Features:**
- OH MY ZSH with robbyrussell theme
- 25 unified plugins
- tmux-manager script
- AI coder suite
- HAS integration scripts

📖 See [reference-minipc/README.md](./reference-minipc/README.md) for complete documentation

---

### 2. **tmux-manager.sh**
**Purpose:** Documented reference for tmux session manager
**Source:** Copied from minipc
**Deployment:** Should be placed in `~/bin/tmux-manager` on all servers

**Features:**
- Interactive menu on SSH login
- Smart session detection and attachment
- Custom session naming
- Skip option for non-tmux users

**Integrated with:**
- `.zshrc` (ZSH servers: Aspire, HAS, minipc)
- `.bashrc` (Bash servers: LLMS)

**Status:** ✅ Deployed to all servers

---

### 3. **omz-unified-config.zsh**
**Purpose:** Standalone OH MY ZSH configuration reference
**Source:** Extracted from minipc .zshrc
**Contains:**
- Theme configuration (robbyrussell)
- 25 unified plugins
- Plugin installation instructions
- Deployment guidelines
- Server-specific customization notes

**Usage:** Reference for OH MY ZSH setup on new servers

**Status:** ✅ Applied to all servers

---

### 4. **tmux-autostart-menu.sh** (Deprecated)
**Status:** 🚫 DEPRECATED - DO NOT USE
**Reason:** Replaced by tmux-manager.sh (minipc reference)
**Kept for:** Historical reference only

---

## 🌐 Deployment Status

| Server | Config Source | tmux-manager | OH MY ZSH | Status |
|--------|--------------|--------------|-----------|--------|
| **minipc** | Reference | ✅ Original | ✅ Reference | 🟢 Reference |
| **Aspire** | minipc | ✅ Deployed | ✅ Unified | 🟢 Unified |
| **HAS** | minipc | ✅ Deployed | ✅ Unified | 🟢 Unified |
| **LLMS** | minipc | ✅ Deployed | ✅ Installed | 🟢 Unified |

---

## 🚀 Deployment Guide

### For New Server Setup

1. **Install OH MY ZSH:**
   ```bash
   sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
   ```

2. **Install Custom Plugins:**
   ```bash
   git clone https://github.com/zsh-users/zsh-autosuggestions \
     ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions
   
   git clone https://github.com/zsh-users/zsh-syntax-highlighting.git \
     ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting
   ```

3. **Deploy tmux-manager:**
   ```bash
   mkdir -p ~/bin
   cp reference-minipc/bin/tmux-manager ~/bin/
   chmod +x ~/bin/tmux-manager
   ```

4. **Configure Shell:**
   ```bash
   # For ZSH (.zshrc):
   # Copy theme and plugins section from omz-unified-config.zsh
   # Add tmux-manager call:
   if [[ -n "$SSH_CONNECTION" ]] && [[ -z "$TMUX" ]] && [[ $- == *i* ]]; then
       ~/bin/tmux-manager
   fi
   ```

5. **Verify:**
   ```bash
   echo $ZSH_THEME  # Should be: robbyrussell
   echo $plugins    # Should match unified set
   ssh <server>     # Should show tmux-manager menu
   ```

---

## 🔄 Update Procedures

### When minipc Config Changes

1. **Capture new reference:**
   ```bash
   ssh minipc "cat ~/.zshrc" > reference-minipc/.zshrc
   ssh minipc "cat ~/bin/tmux-manager" > reference-minipc/bin/tmux-manager
   ```

2. **Update standalone configs:**
   ```bash
   # Update omz-unified-config.zsh if OH MY ZSH changed
   # Update tmux-manager.sh if tmux script changed
   ```

3. **Document changes:**
   ```bash
   # Add entry to docs/CHANGELOG-YYYY-MM-DD.md
   git add -A
   git commit -m "config: Update reference from minipc"
   ```

4. **Propagate to other servers:**
   ```bash
   # Deploy to Aspire, HAS, LLMS as needed
   # Test thoroughly before deployment
   ```

---

## 📚 Configuration Philosophy

### Design Principles

1. **Single Source of Truth:** minipc is the reference
2. **Modularity:** Scripts in ~/bin/, not inline
3. **Simplicity:** Lightweight, fast, reliable
4. **Consistency:** Same UX across all servers
5. **Documentation:** Every config is documented
6. **Versioning:** All changes tracked in git

### Why These Choices?

**robbyrussell theme:**
- No Powerline fonts required
- Fast startup
- Works everywhere
- Clean git status

**25 plugins (not more):**
- Balance functionality vs speed
- All plugins serve clear purpose
- No bloat or unused features

**External tmux-manager:**
- Easier to maintain
- Reusable across servers
- Clean shell RC files
- Simple to update

---

## 🔧 Maintenance

### Regular Tasks

**Monthly:**
- ✅ Verify all servers match reference
- ✅ Update OH MY ZSH: `omz update`
- ✅ Check for plugin updates

**When Adding Server:**
- ✅ Follow deployment guide above
- ✅ Add to deployment status table
- ✅ Document in CHANGELOG

**When Modifying Config:**
- ✅ Update minipc first
- ✅ Capture to reference-minipc/
- ✅ Update standalone configs
- ✅ Propagate to other servers
- ✅ Document changes

### Backup Strategy

**All configs in git:**
- Automatic version history
- Easy rollback: `git checkout <commit>`
- Collaboration friendly

**Server backups:**
- Automatic .backup files on edit
- Manual backups before major changes

---

## 📖 Documentation Index

- [reference-minipc/README.md](./reference-minipc/README.md) - Complete minipc reference
- [../docs/CHANGELOG-2025-11-12-unified-config.md](../docs/CHANGELOG-2025-11-12-unified-config.md) - Unification changelog
- [../ssh-keys-export/TERMUX_SETUP.md](../ssh-keys-export/TERMUX_SETUP.md) - Mobile setup
- omz-unified-config.zsh - OH MY ZSH configuration (this file has inline docs)
- tmux-manager.sh - tmux manager (this file has inline docs)

---

## 🎓 Lessons Learned

### What Worked Well
✅ Using minipc as single reference
✅ External scripts vs inline code
✅ Comprehensive documentation
✅ Automatic backups
✅ Git version control

### What to Improve
⚠️ Automated deployment script
⚠️ Configuration validation tests
⚠️ Automated sync checks

### Future Enhancements
💡 Ansible playbook for deployment
💡 CI/CD for config updates
💡 Monitoring for config drift

---

## 🔒 Security Notes

- SSH keys stored separately in `../ssh-keys-export/`
- No passwords or tokens in configs
- Scripts reviewed for security issues
- File permissions enforced (600 for keys, 755 for scripts)

---

## 📊 Statistics

- **Total config files:** 20+
- **Total scripts:** 16+
- **Servers unified:** 4
- **OH MY ZSH plugins:** 25
- **Documentation files:** 5
- **Git commits:** Tracked
- **Last updated:** 2025-11-12

---

**Maintained by:** Unified Ecosystem Configuration Project
**Status:** ✅ Active and Complete
**Version:** 1.0
