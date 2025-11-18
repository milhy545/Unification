# ============================================================================
# tmux Auto-attach with Menu - Improved Version
# For Unification Project Ecosystem
# Version: 2025-11-12
#
# Features:
# - Attach to existing session by number
# - Create new session
# - Skip tmux (regular shell)
# - 15 second timeout when sessions exist
# - 10 second timeout when no sessions
# ============================================================================

if [[ -n "$SSH_CONNECTION" ]] && [[ -z "$TMUX" ]] && [[ $- == *i* ]]; then
    if ! command -v /usr/bin/tmux &> /dev/null; then
        echo "⚠️  tmux is not installed"
        return
    fi

    echo "🔌 SSH session detected"
    echo ""

    SESSIONS=$(/usr/bin/tmux list-sessions 2>/dev/null)

    if [[ -n "$SESSIONS" ]]; then
        echo "📋 Available tmux sessions:"
        /usr/bin/tmux list-sessions | nl -w2 -s'. '
        echo ""
        echo "Choose: [1-N]=attach session, [N]=new session, [S]=skip tmux"
        read -r -t 15 CHOICE

        # Convert to lowercase for 's' check
        CHOICE_LOWER=$(echo "$CHOICE" | tr '[:upper:]' '[:lower:]')

        if [[ "$CHOICE_LOWER" == "s" ]]; then
            echo "✅ Skipping tmux, regular shell"
        elif [[ "$CHOICE_LOWER" == "n" ]] || [[ -z "$CHOICE" ]]; then
            echo "Creating new session..."
            /usr/bin/tmux new-session -s "ssh-$(date +%Y%m%d-%H%M%S)"
        elif [[ "$CHOICE" =~ ^[0-9]+$ ]]; then
            SESSION_NAME=$(/usr/bin/tmux list-sessions -F '#{session_name}' | sed -n "${CHOICE}p")
            if [[ -n "$SESSION_NAME" ]]; then
                echo "Attaching to session: $SESSION_NAME"
                /usr/bin/tmux attach-session -t "$SESSION_NAME"
            else
                echo "Invalid number, creating new session..."
                /usr/bin/tmux new-session -s "ssh-$(date +%Y%m%d-%H%M%S)"
            fi
        else
            echo "Invalid choice, creating new session..."
            /usr/bin/tmux new-session -s "ssh-$(date +%Y%m%d-%H%M%S)"
        fi
    else
        echo "📋 No existing sessions"
        echo "Choose: [N]=new session, [S]=skip tmux (default: new)"
        read -r -t 10 CHOICE

        CHOICE_LOWER=$(echo "$CHOICE" | tr '[:upper:]' '[:lower:]')

        if [[ "$CHOICE_LOWER" == "s" ]]; then
            echo "✅ Skipping tmux, regular shell"
        else
            echo "Creating default session..."
            /usr/bin/tmux new-session -s "main"
        fi
    fi
fi

# ============================================================================
# DEPLOYMENT INSTRUCTIONS
# ============================================================================
#
# For ZSH (.zshrc):
#   Copy this entire file to the end of ~/.zshrc
#
# For Bash (.bashrc):
#   Copy this entire file to the end of ~/.bashrc
#
# Backup first:
#   cp ~/.zshrc ~/.zshrc.backup.$(date +%Y%m%d_%H%M%S)
#   OR
#   cp ~/.bashrc ~/.bashrc.backup.$(date +%Y%m%d_%H%M%S)
#
# Test:
#   SSH into the server from another machine
#   You should see the tmux menu prompt
#
# Rollback:
#   cp ~/.zshrc.backup.TIMESTAMP ~/.zshrc
#   source ~/.zshrc
