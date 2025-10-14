# TODO: Implementační Plán pro Workstation Setup Wizard

**Cíl:** Vytvořit robustní, idempotentní a "blbuvzdorný" skript `workstation_setup.py`, který automatizuje nastavení vývojářské stanice podle finálního plánu (verze 6).

**Status:** ✅ **DOKONČENO** - Všechny fáze implementovány a otestovány v dry-run režimu

---

## Fáze 0: Příprava a Konfigurace Skriptu

- [x] **Načíst existující kód:** Otevřít a analyzovat stávající soubor `wizards/workstation_setup.py` pro pochopení jeho struktury.
- [x] **Definovat konstanty:** Vytvořit v Python skriptu sekci pro konstanty:
    - [x] Cesta k `dupotEasyFlatpak`: `EASYFLATPAK_DIR = Path.home() / "Programy" / "dupotEasyFlatpak"`
    - [x] Cesta k AppImages: `APPIMAGE_DIR = Path.home() / "AppImages"`
- [x] **Definovat seznamy balíčků:** Vytvořit v Python skriptu jasně definované seznamy (listy) balíčků pro každou kategorii:
    - [x] `APT_CORE_PACKAGES`: Seznam pro jádro systému (35 balíčků)
    - [x] `FLATPAK_APPS`: Seznam aplikací pro instalaci přes `easy-flatpak` (13 aplikací)

---

## Fáze 1: Základní Systém a Prostředí

- [x] **Krok 1.1: Aktualizace APT cache**
    - [x] Implementována metoda `_phase1_update_apt_cache()`
    - [x] Spustit příkaz `sudo apt update`
    - [x] **Ověření:** Zkontrolovat, že příkaz skončil s návratovým kódem 0
    - [x] V případě chyby vrátit False a logovat chybu
    
- [x] **Krok 1.2: Instalace základních závislostí (APT)**
    - [x] Implementována metoda `_phase1_install_basic_dependencies()`
    - [x] Spustit příkaz `sudo apt install -y flatpak git`
    - [x] **Ověření:** Zkontrolovat návratový kód
    - [x] **Ověření:** Spustit `flatpak --version` a ověřit dostupnost
    
- [x] **Krok 1.3: Nastavení `dupotEasyFlatpak`**
    - [x] Implementována metoda `_phase1_setup_easyflatpak()`
    - [x] Zkontrolovat existenci adresáře definovaného v `EASYFLATPAK_DIR`
    - [x] **Pokud neexistuje:**
        - [x] Vytvořit nadřazený adresář
        - [x] Spustit `git clone https://github.com/imikado/dupotEasyFlatpak.git <cesta_k_easyflatpak>`
        - [x] **Ověření:** Znovu zkontrolovat existenci adresáře
    - [x] **Pokud existuje:**
        - [x] Spustit `git -C <cesta_k_easyflatpak> pull` pro zajištění aktuálnosti
        
- [x] **Krok 1.4: Konfigurace Flathub repozitáře**
    - [x] Implementována metoda `_phase1_configure_flathub()`
    - [x] Spustit příkaz `flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo`
    - [x] **Ověření:** Spustit `flatpak remotes` a zkontrolovat, že výstup obsahuje řádek s `flathub`

---

## Fáze 2: Jádro Systému a CLI Nástroje (APT)

- [x] **Krok 2.1: Instalace balíčků z `APT_CORE_PACKAGES`**
    - [x] Implementována metoda `_phase2_install_core_packages()`
    - [x] Sestavit příkaz `sudo apt install -y` spojením všech položek ze seznamu `APT_CORE_PACKAGES`
    - [x] Spustit sestavený příkaz
    - [x] **Ověření:** Zkontrolovat návratový kód
    
- [x] **Krok 2.2: Zajištění repozitáře pro Docker**
    - [x] Implementována metoda `_phase2_setup_docker_repository()`
    - [x] Zkontrolovat existenci souboru `/etc/apt/sources.list.d/docker.list`
    - [x] **Pokud neexistuje:**
        - [x] Vytvořit adresář `/etc/apt/keyrings`
        - [x] Stáhnout a nainstalovat Docker GPG klíč
        - [x] Přidat Docker repozitář do sources.list.d
        - [x] Spustit `sudo apt update`
        
- [x] **Krok 2.3: Nastavení ZSH a Oh My Zsh**
    - [x] Implementována metoda `_phase2_setup_zsh()`
    - [x] Zkontrolovat existenci adresáře `~/.oh-my-zsh`
    - [x] **Pokud neexistuje:**
        - [x] **Upozornění:** Informovat uživatele, že instalace Oh My Zsh může být interaktivní
        - [x] Spustit instalační skript s `--unattended` parametrem
        - [x] **Ověření:** Znovu zkontrolovat existenci adresáře `~/.oh-my-zsh`
        - [x] Nastavit ZSH jako výchozí shell pomocí `chsh -s /usr/bin/zsh`
    - [ ] **TODO (budoucí vylepšení):** Implementovat logiku pro kopírování/symlinkování existujících `.zshrc` konfigurací, pluginů a témat

---

## Fáze 3: Aplikační Vrstva (Flatpak)

- [x] **Krok 3.1: Iterace a instalace aplikací**
    - [x] Implementována metoda `_phase3_install_flatpak_apps()`
    - [x] Vytvořit smyčku, která projde všechny položky v seznamu `FLATPAK_APPS`
    - [x] Pro každou aplikaci:
        - [x] Zkontrolovat existenci `easy-flatpak.sh` skriptu
        - [x] Sestavit příkaz: `<cesta_k_easyflatpak>/easy-flatpak.sh install <nazev_aplikace>`
        - [x] Spustit příkaz
        - [x] **Ověření:** Zkontrolovat návratový kód
        - [x] Logovat úspěch/selhání pro každou aplikaci
        - [x] Pokračovat s dalšími aplikacemi i při selhání jedné

---

## Fáze 4: Speciální Instalace

- [x] **Krok 4.1: Instalace Micromamba**
    - [x] Implementována metoda `_phase4_install_micromamba()`
    - [x] Spustit `command -v micromamba` pro ověření, zda již není nainstalována
    - [x] **Pokud není nalezena:**
        - [x] **Upozornění:** Informovat uživatele o potenciálně interaktivní instalaci
        - [x] Spustit instalační skript: `bash <(curl -L micro.mamba.pm/install.sh)`
        - [x] **Ověření:** Znovu spustit `command -v micromamba` a ověřit úspěch
        
- [x] **Krok 4.2: Instalace Cursor AppImage**
    - [x] Implementována metoda `_phase4_install_cursor_appimage()`
    - [x] Definována URL: `https://downloader.cursor.sh/linux/appImage/x64`
    - [x] Sestavit cílovou cestu: `<cesta_k_appimages>/Cursor.AppImage`
    - [x] Zkontrolovat existenci tohoto souboru
    - [x] **Pokud neexistuje:**
        - [x] Vytvořit adresář pro AppImages
        - [x] Spustit `wget -O <cilova_cesta> <URL_na_appimage>`
        - [x] **Ověření:** Zkontrolovat existenci souboru
    - [x] Spustit `chmod +x <cilova_cesta>` pro udělení oprávnění ke spuštění
    - [x] **Ověření:** Zkontrolovat, že soubor má nastavená oprávnění ke spuštění

---

## Integrace a Workflow

- [x] **Execute Installation Workflow**
    - [x] Refaktorována metoda `execute_installation()` pro volání všech fází sekvenčně
    - [x] Přidáno logování pro každou fázi
    - [x] Implementován error handling s možností pokračovat při non-critical chybách
    - [x] Zachována kompatibilita s legacy kroky (SSH, tmux, AI tools)

- [x] **Dry-Run Support**
    - [x] Všechny metody podporují `dry_run` parametr
    - [x] V dry-run režimu se pouze logují akce bez jejich provedení
    - [x] Umožňuje testování bez změny systému

- [x] **Idempotence**
    - [x] Všechny operace kontrolují existenci před instalací
    - [x] Bezpečné pro opakované spuštění
    - [x] Přeskakují již nainstalované komponenty

---

## Testování

### ✅ Provedené testy:

- [x] Import a inicializace modulu
- [x] Načtení konstant a seznamů balíčků
- [x] Všechny fáze 1-4 v dry-run režimu
- [x] Kompletní workflow execute_installation
- [x] Legacy kroky (SSH, tmux, AI tools)
- [x] Error handling a graceful degradation
- [x] Syntaxe a Pylance validace

### 📋 Zbývající testy (pro produkční nasazení):

- [ ] Skutečná instalace na testovacím systému
- [ ] Edge cases (nedostatek místa, výpadek sítě, chybějící sudo)
- [ ] Rollback při selhání
- [ ] Idempotence - opakované spuštění po částečné instalaci
- [ ] Integrace s master_wizard.py

---

## Git Historie

**Větev:** `blackboxai/implement-workstation-wizard-phases`

**Commity:**
1. `59849b9` - feat: Implementace kompletního workstation setup wizardu podle TODO plánu
2. `c1e2e76` - fix: Robustnější SSH konfigurace v dry-run režimu
3. `5a426c9` - fix: Oprava syntaktické chyby a Pylance warningů

**Status:** Připraveno k pull requestu

---

## Závěr

✅ **Všechny plánované fáze byly úspěšně implementovány a otestovány v dry-run režimu.**

Implementace je:
- ✅ Robustní (error handling, graceful degradation)
- ✅ Idempotentní (bezpečná pro opakované spuštění)
- ✅ "Blbuvzdorná" (kontroly, ověření, logování)
- ✅ Testovatelná (dry-run režim)
- ✅ Dokumentovaná (komentáře, logování)

**Doporučení pro produkční nasazení:**
1. Otestovat na čistém testovacím systému
2. Ověřit všechny edge cases
3. Vytvořit backup před prvním spuštěním
4. Monitorovat logy během instalace
