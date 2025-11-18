# Unified OH MY ZSH Configuration
# Reference: minipc implementation
# Applied to: Aspire, HAS, LLMS, minipc
# Date: 2025-11-12

# ============================================================================
# THEME CONFIGURATION
# ============================================================================

ZSH_THEME="robbyrussell"
# Lightweight, fast, clean theme suitable for all servers
# Alternative themes commented for future reference:
# ZSH_THEME="agnoster"  # More detailed but requires Powerline fonts
# ZSH_THEME="simple"    # Even lighter alternative

# ============================================================================
# PLUGINS CONFIGURATION
# ============================================================================

# Unified plugin set (25 plugins)
# Balance between functionality and performance
plugins=(
    # Version Control
    git

    # Programming Languages
    python
    pip
    node
    npm

    # System & Shell Enhancement
    sudo                        # Double ESC to prefix with sudo
    history                     # Enhanced history management
    colored-man-pages          # Colorized man pages
    command-not-found          # Suggests package for unknown commands
    aliases                    # List all active aliases

    # File Operations
    extract                    # Universal archive extractor
    copyfile                   # Copy file contents to clipboard
    copypath                   # Copy file path to clipboard
    dirhistory                 # Navigate directory history with Alt+arrows

    # Utilities
    encode64                   # Base64 encode/decode
    fzf                       # Fuzzy finder integration
    jsontools                 # JSON pretty-print and validation
    battery                   # Show battery status

    # Enhanced Productivity
    common-aliases            # Useful command shortcuts
    history-substring-search  # Search history with up/down arrows
    magic-enter              # Execute git status on empty line

    # Terminal Management
    tmux                     # tmux integration
    z                        # Smart directory jumping

    # Syntax & Suggestions (must be at end)
    zsh-autosuggestions      # Fish-like autosuggestions
    zsh-syntax-highlighting  # Fish-like syntax highlighting
)

# ============================================================================
# PLUGIN INSTALLATION NOTES
# ============================================================================

# Most plugins are bundled with OH MY ZSH, except:
# - zsh-autosuggestions
# - zsh-syntax-highlighting
#
# Install these custom plugins:
# git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
# git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

# ============================================================================
# OPTIONAL: Server-Specific Additions
# ============================================================================

# For servers with Docker (HAS, Aspire):
# Uncomment to add Docker plugins:
# plugins+=(docker docker-compose)

# For development workstations (Aspire):
# Uncomment to add development tools:
# plugins+=(vscode gh web-search frontend-search)

# For system administration (HAS):
# Uncomment to add system management:
# plugins+=(systemd)

# ============================================================================
# DEPLOYMENT INSTRUCTIONS
# ============================================================================

# 1. Ensure OH MY ZSH is installed:
#    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
#
# 2. Install custom plugins (autosuggestions, syntax-highlighting)
#
# 3. Add this configuration to ~/.zshrc:
#    - Replace ZSH_THEME line
#    - Replace plugins=(...) section
#
# 4. Source the config:
#    source ~/.zshrc
#
# 5. Verify:
#    echo $ZSH_THEME
#    echo $plugins

# ============================================================================
# MAINTENANCE
# ============================================================================

# Update OH MY ZSH and plugins:
# omz update

# List active plugins:
# echo $plugins | tr ' ' '\n'

# Test plugin functionality:
# For each plugin, check its README in ~/.oh-my-zsh/plugins/<plugin-name>/

# ============================================================================
# ROLLBACK
# ============================================================================

# If issues occur, restore default OH MY ZSH config:
# cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc
# Then manually re-apply any custom configurations

# ============================================================================
# VERSION HISTORY
# ============================================================================

# 2025-11-12: Initial unified configuration
#   - Based on minipc reference
#   - 25 plugins
#   - robbyrussell theme
#   - Applied to all servers

# ============================================================================

# END OF UNIFIED OH MY ZSH CONFIGURATION
