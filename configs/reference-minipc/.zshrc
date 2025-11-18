export LC_ALL=C.UTF-8
export ZSH="$HOME/.oh-my-zsh"

# AntiX-specific theme (lighter than agnoster)
ZSH_THEME="robbyrussell"

# Plugins available on AntiX
plugins=(
    git
    python
    pip  
    sudo
    history
    colored-man-pages
    command-not-found
    extract
    copyfile
    copypath
    dirhistory
    encode64
    fzf
    jsontools
    battery
    common-aliases
    history-substring-search
    magic-enter
    aliases
    node
    npm
    tmux
    z
    zsh-autosuggestions
    zsh-syntax-highlighting
)

source $ZSH/oh-my-zsh.sh

# AntiX notebook specific aliases
alias htools="~/start-has-tools"
export PATH=$HOME/bin:$PATH

# Tailscale shortcuts
alias has-ping="ping -c 3 192.168.0.58"  
alias llms-ping="ping -c 3 192.168.0.41"
alias tailscale-status="tailscale status"

# Tmux session manager - spustí se při každém novém terminálu
if [[ -z "$TMUX" ]] && [[ "$TERM_PROGRAM" != "vscode" ]]; then
    echo "🚀 Tmux Session Manager"
    ~/bin/tmux-manager
fi
alias tm="tmux-manager"
alias ai="python3 ~/mycoder-ai.py"
alias fast-ai="python3 ~/mycoder-fast.py"
alias smart-ai="python3 ~/mycoder-smart.py"
alias terminal-ai="python3 ~/mycoder-terminal.py"
alias claude="python3 ~/claude-notebook.py"
alias mycoder="python3 ~/mycoder.py"
alias mycoder="python3 ~/mycoder-ultimate.py"
alias smart="python3 ~/mycoder-ultimate.py"
alias claude-mycoder="python3 ~/mycoder-claude.py"
