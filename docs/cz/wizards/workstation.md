# Průvodce nastavením Workstation

Průvodce nastavením Workstation je klíčovou komponentou frameworku Unification, navrženou pro kompletní automatizaci nastavení vývojové pracovní stanice, specificky přizpůsobené pro stroj typu "Aspire-PC".

## Přehled

Tento průvodce provede uživatele sérií otázek k nastavení nového vývojového prostředí od nuly. Zajišťuje instalaci balíčků, konfiguraci služeb a nastavení specializovaných vývojářských nástrojů. Celý proces je navržen jako **idempotentní**, což znamená, že ho lze bezpečně spustit vícekrát na stejném systému, aniž by došlo k chybám nebo duplicitním konfiguracím.

## Funkce

Průvodce automatizuje následující fáze nastavení:

1.  **Sběr požadavků:** Interaktivně se ptá uživatele, jaké komponenty má nainstalovat a nakonfigurovat.
2.  **Analýza systému:** Detekuje aktuální OS, hardware (včetně speciální detekce pro CPU Q9550) a stav sítě.
3.  **Vytvoření plánu:** Generuje detailní instalační plán s odhadem potřebného času a místa na disku.
4.  **Provedení:** Provádí samotné úpravy systému.
5.  **Validace:** Kontroluje, že všechny konfigurace byly správně aplikovány.

### Detailní akce

-   **Instalace balíčků:**
    -   Instaluje základní sadu požadovaných balíčků (`git`, `python3`, `ssh`, `tmux` atd.).
    -   Volitelně instaluje plnou sadu vývojářských nástrojů (`docker`, `code`, `build-essential` atd.).
    -   Volitelně instaluje balíčky potřebné pro správu napájení na CPU Q9550 (`cpufrequtils`, `lm-sensors`).

-   **Konfigurace SSH serveru:**
    -   Konfiguruje SSH server pro běh na portu `2222`.
    -   Zakazuje přihlášení roota pro zvýšení bezpečnosti.
    -   Zajišťuje, že je služba povolena a běží.

-   **Nastavení ekosystému Tmux:**
    -   Kopíruje standardní konfigurační soubor `.tmux.conf` do domovského adresáře uživatele.
    -   Klonuje repozitář Tmux Plugin Manager (TPM) do `~/.tmux/plugins/tpm`, pokud neexistuje, a připravuje ho tak k použití.

-   **Nastavení AI nástrojů:**
    -   Instaluje předdefinovaný seznam základních Python balíčků pro AI vývoj pomocí `pip`, včetně:
        -   `openai`
        -   `anthropic`
        -   `google-generativeai`
        -   `torch`
        -   `transformers`
        -   `accelerate`

## Jak spustit

Průvodce lze spustit přímo pomocí skriptu `master_wizard.py`:

```bash
# Spuštění v interaktivním módu s výběrem z menu
python3 master_wizard.py

# Přímé spuštění scénáře pro workstation
python3 master_wizard.py --scenario workstation

# Provedení "dry run" bez jakýchkoliv změn v systému
python3 master_wizard.py --scenario workstation --dry-run
```
