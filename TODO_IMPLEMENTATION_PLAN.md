# TODO: Implementační Plán pro Workstation Setup Wizard

**Cíl:** Vytvořit robustní, idempotentní a "blbuvzdorný" skript `workstation_setup.py`, který automatizuje nastavení vývojářské stanice podle finálního plánu (verze 6).

---

## Fáze 0: Příprava a Konfigurace Skriptu

- [ ] **Načíst existující kód:** Otevřít a analyzovat stávající soubor `wizards/workstation_setup.py` pro pochopení jeho struktury.
- [ ] **Definovat konstanty:** Vytvořit v Python skriptu sekci pro konstanty:
    - [ ] Cesta k `dupotEasyFlatpak`: `EASYFLATPAK_DIR = Path.home() / "Programy" / "dupotEasyFlatpak"`
    - [ ] Cesta k AppImages: `APPIMAGE_DIR = Path.home() / "AppImages"`
- [ ] **Definovat seznamy balíčků:** Vytvořit v Python skriptu jasně definované seznamy (listy) balíčků pro každou kategorii:
    - [ ] `APT_CORE_PACKAGES`: Seznam pro jádro systému (Fáze B).
    - [ ] `FLATPAK_APPS`: Seznam aplikací pro instalaci přes `easy-flatpak` (Fáze C).

---

## Fáze 1: Základní Systém a Prostředí

- [ ] **Krok 1.1: Aktualizace APT cache**
    - [ ] Spustit příkaz `sudo apt update`.
    - [ ] **Ověření:** Zkontrolovat, že příkaz skončil s návratovým kódem 0. V případě chyby přerušit a informovat uživatele.
- [ ] **Krok 1.2: Instalace základních závislostí (APT)**
    - [ ] Spustit příkaz `sudo apt install -y flatpak git`.
    - [ ] **Ověření:** Zkontrolovat návratový kód.
    - [ ] **Ověření:** Spustit `flatpak --version` a ověřit, že výstup neobsahuje chybu.
- [ ] **Krok 1.3: Nastavení `dupotEasyFlatpak`**
    - [ ] Zkontrolovat existenci adresáře definovaného v `EASYFLATPAK_DIR`.
    - [ ] **Pokud neexistuje:**
        - [ ] Spustit `git clone https://github.com/imikado/dupotEasyFlatpak.git <cesta_k_easyflatpak>`.
        - [ ] **Ověření:** Znovu zkontrolovat existenci adresáře.
    - [ ] **Pokud existuje:**
        - [ ] Spustit `git -C <cesta_k_easyflatpak> pull` pro zajištění aktuálnosti.
- [ ] **Krok 1.4: Konfigurace Flathub repozitáře**
    - [ ] Spustit příkaz `flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo`.
    - [ ] **Ověření:** Spustit `flatpak remotes` a zkontrolovat, že výstup obsahuje řádek s `flathub`.

---

## Fáze 2: Jádro Systému a CLI Nástroje (APT)

- [ ] **Krok 2.1: Instalace balíčků z `APT_CORE_PACKAGES`**
    - [ ] Sestavit příkaz `sudo apt install -y` spojením všech položek ze seznamu `APT_CORE_PACKAGES`.
    - [ ] Spustit sestavený příkaz.
    - [ ] **Ověření:** Zkontrolovat návratový kód.
- [ ] **Krok 2.2: Zajištění repozitáře pro Docker**
    - [ ] Zkontrolovat existenci souboru `/etc/apt/sources.list.d/docker.list`.
    - [ ] **Pokud neexistuje:**
        - [ ] Provést kroky pro přidání GPG klíče a repozitáře pro Docker (z předchozí analýzy).
        - [ ] Spustit `sudo apt update`.
- [ ] **Krok 1.3: Nastavení `dupotEasyFlatpak`**
    - [ ] Zkontrolovat existenci adresáře definovaného v `EASYFLATPAK_DIR`.
    - [ ] **Pokud neexistuje:**
        - [ ] Spustit `git clone https://github.com/imikado/dupotEasyFlatpak.git <cesta_k_easyflatpak>`.
        - [ ] **Ověření:** Znovu zkontrolovat existenci adresáře.
    - [ ] **Pokud existuje:**
        - [ ] Spustit `git -C <cesta_k_easyflatpak> pull` pro zajištění aktuálnosti.
- [ ] **Krok 1.4: Konfigurace Flathub repozitáře**
    - [ ] Spustit příkaz `flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo`.
    - [ ] **Ověření:** Spustit `flatpak remotes` a zkontrolovat, že výstup obsahuje řádek s `flathub`.

---

## Fáze 2: Jádro Systému a CLI Nástroje (APT)

- [ ] **Krok 2.1: Instalace balíčků z `APT_CORE_PACKAGES`**
    - [ ] Sestavit příkaz `sudo apt install -y` spojením všech položek ze seznamu `APT_CORE_PACKAGES`.
    - [ ] Spustit sestavený příkaz.
    - [ ] **Ověření:** Zkontrolovat návratový kód.
- [ ] **Krok 2.2: Zajištění repozitáře pro Docker**
    - [ ] Zkontrolovat existenci souboru `/etc/apt/sources.list.d/docker.list`.
    - [ ] **Pokud neexistuje:**
        - [ ] Provést kroky pro přidání GPG klíče a repozitáře pro Docker (z předchozí analýzy).
        - [ ] Spustit `sudo apt update`.
- [ ] **Krok 2.3: Nastavení ZSH a Oh My Zsh**
    - [ ] Zkontrolovat existenci adresáře `~/.oh-my-zsh`.
    - [ ] **Pokud neexistuje:**
        - [ ] **Upozornění:** Informovat uživatele, že instalace Oh My Zsh může být interaktivní a vyžaduje jeho pozornost.
        - [ ] Spustit instalační skript: `sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended` (pokus o neinteraktivní instalaci).
        - [ ] **Ověření:** Znovu zkontrolovat existenci adresáře `~/.oh-my-zsh`.
    - [ ] **TODO (vyžaduje další specifikaci):** Implementovat logiku pro kopírování/symlinkování existujících `.zshrc` konfigurací, pluginů a témat.

---

## Fáze 3: Aplikační Vrstva (Flatpak)

- [ ] **Krok 3.1: Iterace a instalace aplikací**
    - [ ] Vytvořit smyčku, která projde všechny položky v seznamu `FLATPAK_APPS`.
    - [ ] Pro každou aplikaci:
        - [ ] Sestavit příkaz: `<cesta_k_easyflatpak>/easy-flatpak.sh install <nazev_aplikace>`.
        - [ ] Spustit příkaz.
        - [ ] **Ověření:** Zkontrolovat návratový kód.
        - [ ] **Ověření (volitelné):** Spustit `flatpak list | grep <id_aplikace>` a ověřit, že se aplikace nachází v seznamu nainstalovaných.

---

## Fáze 4: Speciální Instalace

- [ ] **Krok 4.1: Instalace Micromamba**
    - [ ] Spustit `command -v micromamba` pro ověření, zda již není nainstalována.
    - [ ] **Pokud není nalezena:**
        - [ ] **Upozornění:** Informovat uživatele o potenciálně interaktivní instalaci.
        - [ ] Spustit instalační skript: `bash <(curl -L micro.mamba.pm/install.sh)`.
        - [ ] **Ověření:** Znovu spustit `command -v micromamba` a ověřit úspěch.
- [ ] **Krok 4.2: Instalace Cursor AppImage**
    - [ ] **TODO:** Najít a definovat v konstantách přímou URL na nejnovější verzi Cursor AppImage.
    - [ ] Sestavit cílovou cestu: `<cesta_k_appimages>/Cursor.AppImage`.
    - [ ] Zkontrolovat existenci tohoto souboru.
    - [ ] **Pokud neexistuje:**
        - [ ] Spustit `wget -O <cilova_cesta> <URL_na_appimage>`.
        - [ ] **Ověření:** Zkontrolovat existenci souboru.
    - [ ] Spustit `chmod +x <cilova_cesta>` pro udělení oprávnění ke spuštění.
    - [ ] **Ověření:** Zkontrolovat, že soubor má nastavená oprávnění ke spuštění.

---

Tento plán by měl sloužit jako přesný a spolehlivý manuál pro implementaci. Můžeme začít pracovat na první fázi?
