### Recap: Final Workstation Application List (Version 6)

This list serves as the basis for automated installation using the `workstation_setup.py` script.

#### Category 1: Core Packages (Always Install via APT)
These packages will be installed directly into the system using `apt` for optimal integration and functionality.

*   **Network and Services:**
    *   `openssh-server`
    *   `net-tools`
    *   `tailscale`
    *   `docker-ce`, `docker-ce-cli`, `containerd.io` (for Docker)
    *   `podman-docker` (for Podman)
    *   `qemu-kvm`, `virt-manager` (for virtualization)
*   **Terminal and Shell:**
    *   `tmux`
    *   `alacritty`
    *   `zsh`, `zsh-common` (including Oh My Zsh and configuration)
    *   `ripgrep` (`rg`)
    *   `bat`
    *   `htop`, `iftop`, `iotop`
*   **Development and Compilation:**
    *   `build-essential`
    *   `cmake`
    *   `git`
    *   `gh` (GitHub CLI)
    *   `python3-all`, `python3-pip`
    *   `nodejs`, `npm`
*   **CLI Utilities:**
    *   `sqlite3`
    *   `jq`
    *   `yq`
    *   `shellcheck`

#### Category 2: Applications and IDEs (Install via `dupotEasyFlatpak`)
These applications will be installed as Flatpak packages using the `dupotEasyFlatpak` script.

*   **Editors and IDEs:**
    *   `code` (Visual Studio Code)
    *   `code-insiders` (Visual Studio Code - Insiders version)
    *   `codium` (VSCodium)
    *   `codium-insiders` (VSCodium - Insiders version)
    *   `io.dbeaver.DBeaverCommunity` (DBeaver CE)
    *   `cc.arduino.IDE2` (Arduino IDE)
*   **API Tools:**
    *   `com.getpostman.Postman` (Postman)
    *   `rest.insomnia.Insomnia` (Insomnia)
*   **Browsers and Communication:**
    *   `org.mozilla.firefox` (Firefox)
    *   `org.telegram.desktop` (Telegram Desktop)
    *   `ch.protonmail.protonmail-bridge` (Proton Mail Bridge)
    *   `com.proton.pass` (Proton Pass)
    *   `com.github.tchx84.Flatseal` (Flatseal)

#### Category 3: Special and Scripted Installations
These tools require a unique installation procedure.

*   **`micromamba`**: Installation using its official script.
*   **`Cursor`**: Downloaded as an AppImage and placed in `~/AppImages`.