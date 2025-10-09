# 🚀 Unification - Ultimátní Automatizace Nastavení Systému

## Přehled
Unification je sofistikovaný automatizační framework pro nastavení a správu multi-serverových vývojových prostředí. Vznikl z chaosu 150+ problémů s SSH konfigurací a demonstruje systematické řešení problémů pomocí inteligentní automatizace.

## Klíčové Funkce
- **Automatizované Scénáře Nastavení** - Wizardy pro pracovní stanice, servery a další.
- **Inteligentní Řešení Závislostí** - Chytrá správa balíčků.
- **Síťová Topologie Intelligence** - Automatická detekce a konfigurace serverových ekosystémů.
- **Dvojjazyčná Dokumentace** - Kompletní průvodci v angličtině (`README.md`) a češtině (`README.cz.md`).

## Struktura Projektu
```
Unification/
├── master_wizard.py          # Hlavní vstupní bod pro všechny scénáře
├── wizards/                  # Jednotlivé setup wizardy
│   └── workstation_setup.py  # --> Implementace probíhá
├── tools/                    # Společné utility (detekce systému, validace, atd.)
│   ├── system_detector.py
│   ├── dependency_resolver.py
│   ├── network_scanner.py
│   └── config_validator.py
├── configs/                  # Šablony konfigurací
│   └── tmux.conf             # --> První implementovaná konfigurace
├── tests/                    # Testy pro všechny komponenty
└── docs/                     # Soubory s dokumentací
    ├── stories/
    └── ...
```

## Aktuální Stav
Projekt je v počáteční fázi vývoje. Základní framework a hlavní wizard `workstation_setup` se aktivně vyvíjí.
- **✅ Implementováno:**
  - Základní struktura projektu s wizardy a nástroji.
  - **Nasazení konfigurace pro tmux** v rámci `workstation_setup` wizardu.
- **Probíhá:**
  - Restrukturalizace a aktualizace dokumentace.
  - Implementace dalších kroků podle roadmapy.

## Roadmapa
Následující funkce jsou plánovány k implementaci, primárně v rámci `workstation_setup` wizardu:

1.  **Konfigurace SSH Serveru:** Implementovat funkci `_configure_ssh_server` pro bezpečné nastavení `sshd_config`.
2.  **Správa Napájení:** Implementovat `_setup_power_management` pro řízení teploty a napájení procesoru Q9550.
3.  **Nastavení AI Nástrojů:** Implementovat `_setup_ai_tools` pro instalaci a konfiguraci vývojového prostředí pro AI.
4.  **Nastavení Aliasů a Shellu:** Přidat krok pro nasazení unifikovaných aliasů a konfigurací shellu (např. `.bash_aliases`, `.zshrc`).
5.  **Rozšíření Wizardů:** Po dokončení `workstation_setup` bude zahájen vývoj dalších plánovaných wizardů (`llm_server_setup`, `database_setup`, atd.).

## Rychlý Start
```bash
git clone https://github.com/milhy545/Unification.git
cd Unification
python3 master_wizard.py
```

## Licence
Soukromý repozitář - Projekt pro portfolio a demonstraci.

---
*Vytvořeno k řešení reálných výzev v oblasti automatizace infrastruktury.*
*Vyvinuto s poznatky získanými z více než 150 bitev s konfigurací SSH.*
