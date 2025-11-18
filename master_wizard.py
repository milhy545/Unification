#!/usr/bin/env python3
"""
Unifikation Master Wizard - Ultimate System Setup Automation
Entry point for intelligent multi-server environment setup
"""

import sys
import argparse
import logging
# from typing import Dict, List, Optional  # Currently unused
from dataclasses import dataclass
from enum import Enum

from tools.system_detector import SystemDetector
from tools.dependency_resolver import DependencyResolver
from tools.network_scanner import NetworkScanner
from tools.config_validator import ConfigValidator
from tools.preconditions import explain_environment
from tools import __init__ as tools_init  # keep namespace import stable
from tools import preconditions as _pre
from tools.i18n import get as _t


class SetupScenario(Enum):
    """Available setup scenarios for different server types."""
    WORKSTATION = "workstation"
    LLM_SERVER = "llm_server"
    ORCHESTRATION = "orchestration"
    DATABASE = "database"
    MONITORING = "monitoring"


@dataclass
class MenuOption:
    """Bilingual menu option definition."""
    en: str
    cz: str
    scenario: SetupScenario


class MasterWizard:
    """Main wizard orchestrating all setup scenarios."""

    MENU_OPTIONS = {
        1: MenuOption(
            en="💻 Workstation Setup - Development powerhouse",
            cz="💻 Nastavení Workstation - Vývojová stanice",
            scenario=SetupScenario.WORKSTATION
        ),
        2: MenuOption(
            en="🧠 LLM Server Setup - AI processing unit",
            cz="🧠 Nastavení LLM Server - AI jednotka",
            scenario=SetupScenario.LLM_SERVER
        ),
        3: MenuOption(
            en="🏠 Orchestration Setup - Home automation hub",
            cz="🏠 Nastavení Orchestrace - Centrum domácí automatizace",
            scenario=SetupScenario.ORCHESTRATION
        ),
        4: MenuOption(
            en="🗄️ Database Server Setup - Data management hub",
            cz="🗄️ Nastavení Databázového serveru - Centrum dat",
            scenario=SetupScenario.DATABASE
        ),
        5: MenuOption(
            en="📊 Monitoring Setup - Observability center",
            cz="📊 Nastavení Monitoringu - Centrum sledování",
            scenario=SetupScenario.MONITORING
        )
    }

    ADDITIONAL_OPTIONS = {
        6: MenuOption(
            en="🔧 Add Machine to Ecosystem - Integrate existing machine",
            cz="🔧 Přidat Stroj do Ekosystému - Integrovat existující stroj",
            scenario=None
        ),
        7: MenuOption(
            en="🔄 Post-Reinstall Recovery - Restore after OS reinstall",
            cz="🔄 Obnova po Reinstalaci - Obnovit po reinstalaci OS",
            scenario=None
        ),
        8: MenuOption(
            en="🩺 System Health Check - Validate entire ecosystem",
            cz="🩺 Kontrola Zdraví Systému - Validace celého ekosystému",
            scenario=None
        )
    }

    def __init__(self, language: str = "en"):
        """Initialize master wizard with language preference."""
        self.language = language
        self.system_detector = SystemDetector()
        self.dependency_resolver = DependencyResolver()
        self.network_scanner = NetworkScanner()
        self.config_validator = ConfigValidator()
        self.setup_logging()

    def setup_logging(self):
        """Configure logging for the wizard."""
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler('unification.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def display_banner(self):
        """Display welcome banner with language selection (localized)."""
        env = explain_environment()
        env_line = f"root={env.get('is_root')}, net={env.get('network')}, apt={env.get('has_apt')}, pacman={env.get('has_pacman')}, apk={env.get('has_apk')}"
        banner = f"""
🚀 {_t('banner_title', self.language, 'UNIFICATION SYSTEM SETUP')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ultimate Multi-Server Environment Setup Automation
Born from 150+ SSH configuration battles

System detected: {self.get_system_summary()}
Available ecosystems: {self.get_network_summary()}
{_t('info_env_summary', self.language, 'Environment summary')}: {env_line}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        print(banner)

    def get_system_summary(self) -> str:
        """Get brief system information summary."""
        try:
            info = self.system_detector.detect_basic_info()
            return f"{info.get('os', 'Unknown')} on {info.get('arch', 'Unknown')}"
        except Exception as e:
            self.logger.warning(f"Could not detect system info: {e}")
            return "Detection failed"

    def get_network_summary(self) -> str:
        """Get brief network ecosystem summary."""
        try:
            servers = self.network_scanner.scan_ecosystem()
            return f"{len(servers)} servers discovered"
        except Exception as e:
            self.logger.warning(f"Could not scan network: {e}")
            return "Network scan failed"

    def display_menu(self):
        """Display interactive menu in selected language."""
        print("\nChoose your setup scenario / Vyberte scénář nastavení:\n")

        # Main scenarios
        for num, option in self.MENU_OPTIONS.items():
            text = option.cz if self.language == "cz" else option.en
            print(f"{num}. {text}")

        print()  # Separator

        # Additional options
        for num, option in self.ADDITIONAL_OPTIONS.items():
            text = option.cz if self.language == "cz" else option.en
            print(f"{num}. {text}")

        print("\n0. Exit / Ukončit")

    def get_user_choice(self) -> int:
        """Get and validate user menu choice."""
        while True:
            try:
                choice = input("\nEnter your choice / Zadejte volbu (0-8): ")
                choice_num = int(choice)

                if 0 <= choice_num <= 8:
                    return choice_num
                else:
                    print("Invalid choice. Please enter 0-8 / Neplatná volba. Zadejte 0-8")

            except ValueError:
                print("Please enter a number / Zadejte číslo")
            except KeyboardInterrupt:
                print("\n\nExiting... / Ukončuji...")
                sys.exit(0)

    def execute_scenario(self, scenario: SetupScenario, dry_run: bool = False):
        """Execute the selected setup scenario."""
        self.logger.info(f"Starting setup scenario: {scenario.value} (dry_run={dry_run})")

        scenario_modules = {
            SetupScenario.WORKSTATION: "wizards.workstation_setup",
            SetupScenario.LLM_SERVER: "wizards.llm_server_setup",
            SetupScenario.ORCHESTRATION: "wizards.orchestration_setup",
            SetupScenario.DATABASE: "wizards.database_setup",
            SetupScenario.MONITORING: "wizards.monitoring_setup"
        }

        try:
            module_name = scenario_modules[scenario]
            module = __import__(module_name, fromlist=[''])
            wizard_class = getattr(module, f"{scenario.value.title().replace('_', '')}Wizard")

            wizard = wizard_class(language=self.language)
            wizard.run_setup(dry_run=dry_run)

        except ImportError as e:
            self.logger.error(f"Could not import wizard module: {e}")
            print(f"Setup scenario not yet implemented: {scenario.value}")
        except Exception as e:
            self.logger.error(f"Setup failed: {e}")
            print(f"Setup failed: {e}")

    def execute_ecosystem_integration(self):
        """Add existing machine to ecosystem."""
        print("🔧 Ecosystem Integration - Coming soon...")

    def execute_post_reinstall_recovery(self):
        """Recover system after OS reinstall."""
        print("🔄 Post-Reinstall Recovery - Coming soon...")

    def execute_health_check(self):
        """Perform comprehensive ecosystem health check (localized output)."""
        # Lokalizované popisky
        lang = self.language
        start_msg = "🩺 Spouštím kontrolu zdraví ekosystému..." if lang == "cz" else "🩺 Running ecosystem health check..."
        sys_ok = "✅ V pořádku" if lang == "cz" else "✅ OK"
        sys_bad = "❌ Nalezeny problémy" if lang == "cz" else "❌ Issues detected"
        net_bad = "❌ Problémy s konektivitou" if lang == "cz" else "❌ Connection issues"
        conf_bad = "❌ Problémy v konfiguraci" if lang == "cz" else "❌ Config issues"
        section_system = "Zdraví systému" if lang == "cz" else "System Health"
        section_network = "Zdraví sítě" if lang == "cz" else "Network Health"
        section_config = "Konfigurace" if lang == "cz" else "Configuration Health"
        summary_hdr = "Souhrn doporučení" if lang == "cz" else "Recommendations summary"

        print(start_msg)

        try:
            # System health
            system_status = self.system_detector.health_check()
            print(f"{section_system}: {sys_ok if system_status else sys_bad}")

            # Network connectivity
            network_status = self.network_scanner.connectivity_check()
            print(f"{section_network}: {sys_ok if network_status else net_bad}")

            # Configuration validation + stručný report
            config_status = self.config_validator.validate_ecosystem()
            print(f"{section_config}: {sys_ok if config_status else conf_bad}")

            # Volitelně vypíšeme krátký souhrn z detailního reportu
            try:
                report = self.config_validator.generate_validation_report()
                if report.recommendations:
                    print(f"\n{summary_hdr}:")
                    # vytisknout max 5 doporučení
                    for rec in report.recommendations[:5]:
                        print(f" - {rec}")
            except Exception as rep_e:
                self.logger.debug(f"Could not generate detailed validation report: {rep_e}")

        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            print(("Kontrola zdraví selhala: " if lang == "cz" else "Health check failed: ") + str(e))

    def run(self, dry_run: bool = False):
        """Main wizard execution loop."""
        self.display_banner()

        while True:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == 0:
                print("Goodbye! / Na shledanou!")
                break

            elif choice in self.MENU_OPTIONS:
                option = self.MENU_OPTIONS[choice]
                self.execute_scenario(option.scenario, dry_run=dry_run)

            elif choice == 6:
                self.execute_ecosystem_integration()
            elif choice == 7:
                self.execute_post_reinstall_recovery()
            elif choice == 8:
                self.execute_health_check()

            input("\nPress Enter to continue / Stiskněte Enter pro pokračování...")


def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        # description="Unification Master Wizard - Ultimate System Setup Automation"
    )
    parser.add_argument(
        "--language", "-l",
        choices=["en", "cz"],
        default="en",
        help="Interface language (en/cz)"
    )
    parser.add_argument(
        "--scenario", "-s",
        choices=[s.value for s in SetupScenario],
        help="Run specific scenario directly"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--dry-run", "-d",
        action="store_true",
        help="Simulate execution without making system changes"
    )

    args = parser.parse_args()

    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Create and run wizard
    wizard = MasterWizard(language=args.language)

    if args.scenario:
        # Direct scenario execution
        scenario = SetupScenario(args.scenario)
        wizard.execute_scenario(scenario, dry_run=args.dry_run)
    else:
        # Interactive mode
        wizard.run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
