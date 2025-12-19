### Rekapitulace: Finální Seznam Aplikací pro Workstation Setup (Verze 6)

Tento seznam slouží jako základ pro automatizovanou instalaci pomocí `workstation_setup.py` skriptu.

#### Kategorie 1: Základní balíčky (Instalovat vždy přes APT)
Tyto balíčky budou instalovány přímo do systému pomocí `apt` pro zajištění nejlepší integrace a funkčnosti.

*   **Síť a Služby:**
    *   `openssh-server`
    *   `net-tools`
    *   `tailscale`
    *   `docker-ce`, `docker-ce-cli`, `containerd.io` (pro Docker)
    *   `podman-docker` (pro Podman)
    *   `qemu-kvm`, `virt-manager` (pro virtualizaci)
*   **Terminál a Shell:**
    *   `tmux`
    *   `alacritty`
    *   `zsh`, `zsh-common` (včetně Oh My Zsh a konfigurace)
    *   `ripgrep` (`rg`)
    *   `bat`
    *   `htop`, `iftop`, `iotop`
*   **Vývoj a Kompilace:**
    *   `build-essential`
    *   `cmake`
    *   `git`
    *   `gh` (GitHub CLI)
    *   `python3-all`, `python3-pip`
    *   `nodejs`, `npm`
*   **CLI Utility:**
    *   `sqlite3`
    *   `jq`
    *   `yq`
    *   `shellcheck`

#### Kategorie 2: Aplikace a IDE (Instalovat přes `dupotEasyFlatpak`)
Tyto aplikace budou instalovány jako Flatpak balíčky pomocí skriptu `dupotEasyFlatpak`.

*   **Editory a IDE:**
    *   `code` (Visual Studio Code)
    *   `code-insiders` (Visual Studio Code - Insiders verze)
    *   `codium` (VSCodium)
    *   `codium-insiders` (VSCodium - Insiders verze)
    *   `io.dbeaver.DBeaverCommunity` (DBeaver CE)
    *   `cc.arduino.IDE2` (Arduino IDE)
*   **API Nástroje:**
    *   `com.getpostman.Postman` (Postman)
    *   `rest.insomnia.Insomnia` (Insomnia)
*   **Prohlížeče a Komunikace:**
    *   `org.mozilla.firefox` (Firefox)
    *   `org.telegram.desktop` (Telegram Desktop)
    *   `ch.protonmail.protonmail-bridge` (Proton Mail Bridge)
    *   `com.proton.pass` (Proton Pass)
    *   `com.github.tchx84.Flatseal` (Flatseal)

#### Kategorie 3: Speciální a skriptované instalace
Tyto nástroje vyžadují unikátní postup instalace.

*   **`micromamba`**: Instalace pomocí oficiálního skriptu.
*   **`Cursor`**: Stáhne se jako AppImage a bude umístěn do `~/AppImages`.