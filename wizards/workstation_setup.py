"""
Workstation Setup Wizard
Automated setup for development workstation (Aspire PC type)
"""

import os
import sys
import logging
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass

from tools.system_detector import SystemDetector
from tools.dependency_resolver import DependencyResolver
from tools.network_scanner import NetworkScanner
from tools.config_validator import ConfigValidator


@dataclass
class WorkstationConfig:
    """Workstation configuration parameters."""
    hostname: str
    enable_ssh_server: bool = True
    ssh_port: int = 2222
    install_development_tools: bool = True
    setup_tmux_ecosystem: bool = True
    configure_power_management: bool = True
    setup_ai_tools: bool = True
    enable_monitoring: bool = True


class WorkstationWizard:
    """Intelligent workstation setup wizard."""

    # Fáze 0: Konstanty pro cesty
    EASYFLATPAK_DIR = Path.home() / "Programy" / "dupotEasyFlatpak"
    APPIMAGE_DIR = Path.home() / "AppImages"
    
    # Fáze 0: Seznamy balíčků
    # Category 1: Core Packages (APT)
    APT_CORE_PACKAGES = [
        # Network and Services
        "openssh-server",
        "net-tools",
        "tailscale",
        "docker-ce", "docker-ce-cli", "containerd.io",
        "podman-docker",
        "qemu-kvm", "virt-manager",
        # Terminal and Shell
        "tmux",
        "alacritty",
        "zsh", "zsh-common",
        "ripgrep",
        "bat",
        "htop", "iftop", "iotop",
        # Development and Compilation
        "build-essential",
        "cmake",
        "git",
        "gh",
        "python3-all", "python3-pip",
        "nodejs", "npm",
        # CLI Utilities
        "sqlite3",
        "jq",
        "yq",
        "shellcheck",
        # Additional dependencies
        "curl", "wget",
        "flatpak",
        "cpufrequtils", "lm-sensors"  # For power management
    ]
    
    # Category 2: Flatpak Applications (via dupotEasyFlatpak)
    FLATPAK_APPS = [
        # Editors and IDEs
        "code",
        "code-insiders",
        "codium",
        "codium-insiders",
        "io.dbeaver.DBeaverCommunity",
        "cc.arduino.IDE2",
        # API Tools
        "com.getpostman.Postman",
        "rest.insomnia.Insomnia",
        # Browsers and Communication
        "org.mozilla.firefox",
        "org.telegram.desktop",
        "ch.protonmail.protonmail-bridge",
        "com.proton.pass",
        "com.github.tchx84.Flatseal"
    ]

    # Legacy package lists (kept for backward compatibility)
    REQUIRED_PACKAGES = [
        "git", "python3", "pip", "curl", "wget", "ssh", "sshd",
        "tmux", "htop", "nodejs", "npm"
    ]

    DEVELOPMENT_PACKAGES = [
        "docker", "code", "firefox", "vim", "nano", "build-essential",
        "python3-dev", "python3-venv"
    ]

    AI_TOOLS_PACKAGES = [
        "python3-pip", "python3-dev", "ffmpeg", "git-lfs"
    ]

    def __init__(self, language: str = "en"):
        """Initialize workstation wizard."""
        self.language = language
        self.system_detector = SystemDetector()
        self.dependency_resolver = DependencyResolver()
        self.network_scanner = NetworkScanner()
        self.config_validator = ConfigValidator()
        self.setup_logging()

    def setup_logging(self):
        """Configure logging for the wizard."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('workstation_setup.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def gather_requirements(self, dry_run: bool = False) -> WorkstationConfig:
        """Gather workstation setup requirements from user."""
        self.logger.info("Gathering workstation setup requirements")

        if dry_run:
            # Use default values for dry run
            return WorkstationConfig(
                hostname="Aspire-PC",
                enable_ssh_server=True,
                install_development_tools=True,
                setup_ai_tools=True,
                configure_power_management=True
            )

        if self.language == "cz":
            print("\n🖥️ NASTAVENÍ VÝVOJOVÉ WORKSTATION")
            print("=" * 50)
            try:
                hostname = input("Název počítače [Aspire-PC]: ") or "Aspire-PC"
            except EOFError:
                hostname = "Aspire-PC"

            try:
                ssh_prompt = "Povolit SSH server? (y/n) [y]: "
                ssh_input = input(ssh_prompt).lower()
                enable_ssh = ssh_input in ['', 'y', 'yes', 'ano']
            except EOFError:
                enable_ssh = True

            try:
                dev_prompt = "Nainstalovat vývojové nástroje? (y/n) [y]: "
                dev_input = input(dev_prompt).lower()
                install_dev = dev_input in ['', 'y', 'yes', 'ano']
            except EOFError:
                install_dev = True

            try:
                ai_prompt = "Nastavit AI nástroje (Claude, etc.)? (y/n) [y]: "
                ai_input = input(ai_prompt).lower()
                setup_ai = ai_input in ['', 'y', 'yes', 'ano']
            except EOFError:
                setup_ai = True

            try:
                power_prompt = "Nastavit Q9550 power management? (y/n) [y]: "
                power_input = input(power_prompt).lower()
                setup_power = power_input in ['', 'y', 'yes', 'ano']
            except EOFError:
                setup_power = True

        else:
            print("\n💻 WORKSTATION SETUP")
            print("=" * 30)
            try:
                hostname = input("Computer hostname [Aspire-PC]: ") or "Aspire-PC"
            except EOFError:
                hostname = "Aspire-PC"

            try:
                ssh_input = input("Enable SSH server? (y/n) [y]: ").lower()
                enable_ssh = ssh_input in ['', 'y', 'yes']
            except EOFError:
                enable_ssh = True

            try:
                dev_input = input("Install development tools? (y/n) [y]: ").lower()
                install_dev = dev_input in ['', 'y', 'yes']
            except EOFError:
                install_dev = True

            try:
                ai_input = input("Setup AI tools (Claude, etc.)? (y/n) [y]: ").lower()
                setup_ai = ai_input in ['', 'y', 'yes']
            except EOFError:
                setup_ai = True

            try:
                power_input = input("Setup Q9550 power management? (y/n) [y]: ").lower()
                setup_power = power_input in ['', 'y', 'yes']
            except EOFError:
                setup_power = True

        return WorkstationConfig(
            hostname=hostname,
            enable_ssh_server=enable_ssh,
            install_development_tools=install_dev,
            setup_ai_tools=setup_ai,
            configure_power_management=setup_power
        )

    def analyze_system(self) -> Dict:
        """Analyze current system state."""
        self.logger.info("Analyzing system configuration")

        # Detect system information
        system_info = self.system_detector.detect_comprehensive_info()
        thermal_info = self.system_detector.detect_thermal_capabilities()
        security_info = self.system_detector.detect_security_features()

        # Detect network topology
        network_topology = self.network_scanner.discover_network_topology()

        # Validate current configuration
        validation_report = self.config_validator.generate_validation_report()

        analysis = {
            "system": system_info,
            "thermal": thermal_info,
            "security": security_info,
            "network": network_topology,
            "validation": validation_report,
            "q9550_detected": thermal_info.get("q9550_detected", False),
            "existing_ecosystem": len(network_topology.ecosystem_servers) > 0
        }

        # Display analysis results
        if self.language == "cz":
            print("\n📊 ANALÝZA SYSTÉMU")
            print(f"• OS: {system_info.os_name}")
            print(f"• CPU: {system_info.cpu_cores} jader @ {system_info.cpu_frequency:.1f} MHz")
            print(f"• RAM: {system_info.memory_total // (1024**3)} GB")
            print(f"• Q9550 detekováno: {'✅' if analysis['q9550_detected'] else '❌'}")
            print(f"• Existující ecosystem: {len(network_topology.ecosystem_servers)} serverů")
        else:
            print("\n📊 SYSTEM ANALYSIS")
            print(f"• OS: {system_info.os_name}")
            print(f"• CPU: {system_info.cpu_cores} cores @ {system_info.cpu_frequency:.1f} MHz")
            print(f"• RAM: {system_info.memory_total // (1024**3)} GB")
            print(f"• Q9550 detected: {'✅' if analysis['q9550_detected'] else '❌'}")
            print(f"• Existing ecosystem: {len(network_topology.ecosystem_servers)} servers")

        return analysis

    def create_installation_plan(self, config: WorkstationConfig, analysis: Dict) -> Dict:
        """Create detailed installation plan."""
        self.logger.info("Creating installation plan")

        # Base packages
        packages_to_install = self.REQUIRED_PACKAGES.copy()

        # Add optional packages based on configuration
        if config.install_development_tools:
            packages_to_install.extend(self.DEVELOPMENT_PACKAGES)

        if config.setup_ai_tools:
            packages_to_install.extend(self.AI_TOOLS_PACKAGES)

        # Resolve dependencies
        installation_plan = self.dependency_resolver.resolve_dependencies(packages_to_install)

        # Configuration steps
        config_steps = []

        if config.enable_ssh_server:
            config_steps.append({
                "name": "configure_ssh",
                "description": "Configure SSH server on port 2222",
                "estimated_time": 60
            })

        if config.setup_tmux_ecosystem:
            config_steps.append({
                "name": "setup_tmux",
                "description": "Configure tmux ecosystem integration",
                "estimated_time": 120
            })

        if config.configure_power_management and analysis["q9550_detected"]:
            config_steps.append({
                "name": "setup_power_management",
                "description": "Configure Q9550 thermal management",
                "estimated_time": 180
            })
            packages_to_install.extend(["cpufrequtils", "lm-sensors"])

        if config.setup_ai_tools:
            config_steps.append({
                "name": "setup_ai_tools",
                "description": "Configure AI development environment",
                "estimated_time": 300
            })

        total_time = (installation_plan.estimated_time +
                     sum(step["estimated_time"] for step in config_steps))

        plan = {
            "packages": installation_plan,
            "configuration_steps": config_steps,
            "total_estimated_time": total_time,
            "disk_space_required": installation_plan.disk_space_required + 1000,  # +1GB for configs
            "conflicts": installation_plan.conflicts_detected,
            "warnings": []
        }

        # Add warnings
        if analysis["validation"].overall_status == "error":
            plan["warnings"].append("System has configuration errors that need fixing")

        if not analysis["security"]["sudo_available"]:
            plan["warnings"].append("Sudo access required for system configuration")

        return plan

    def display_installation_plan(self, plan: Dict):
        """Display installation plan to user."""
        if self.language == "cz":
            print("\n📋 INSTALAČNÍ PLÁN")
            print(f"• Balíčky k instalaci: {len(plan['packages'].packages_to_install)}")
            print(f"• Konfigurační kroky: {len(plan['configuration_steps'])}")
            print(f"• Odhadovaný čas: {plan['total_estimated_time']//60} minut")
            print(f"• Potřebný diskový prostor: {plan['disk_space_required']} MB")

            if plan['conflicts']:
                print(f"⚠️  Konflikty: {len(plan['conflicts'])}")
                for conflict in plan['conflicts']:
                    print(f"   • {conflict}")

            if plan['warnings']:
                print("⚠️  Upozornění:")
                for warning in plan['warnings']:
                    print(f"   • {warning}")

        else:
            print("\n📋 INSTALLATION PLAN")
            print(f"• Packages to install: {len(plan['packages'].packages_to_install)}")
            print(f"• Configuration steps: {len(plan['configuration_steps'])}")
            print(f"• Estimated time: {plan['total_estimated_time']//60} minutes")
            print(f"• Disk space required: {plan['disk_space_required']} MB")

            if plan['conflicts']:
                print(f"⚠️  Conflicts: {len(plan['conflicts'])}")
                for conflict in plan['conflicts']:
                    print(f"   • {conflict}")

            if plan['warnings']:
                print("⚠️  Warnings:")
                for warning in plan['warnings']:
                    print(f"   • {warning}")

    def execute_installation(self, plan: Dict, config: WorkstationConfig, dry_run: bool = False):
        """Execute the installation plan podle TODO_IMPLEMENTATION_PLAN.md."""
        self.logger.info(f"Executing installation plan (dry_run={dry_run})")

        try:
            # ========== FÁZE 1: Základní Systém a Prostředí ==========
            self.logger.info("=" * 60)
            self.logger.info("FÁZE 1: Základní Systém a Prostředí")
            self.logger.info("=" * 60)
            
            # Fáze 1.1: Aktualizace APT cache
            if not self._phase1_update_apt_cache(dry_run):
                raise Exception("Fáze 1.1 selhala: APT cache update")
            
            # Fáze 1.2: Instalace základních závislostí
            if not self._phase1_install_basic_dependencies(dry_run):
                raise Exception("Fáze 1.2 selhala: Základní závislosti")
            
            # Fáze 1.3: Setup dupotEasyFlatpak
            if not self._phase1_setup_easyflatpak(dry_run):
                raise Exception("Fáze 1.3 selhala: dupotEasyFlatpak setup")
            
            # Fáze 1.4: Konfigurace Flathub
            if not self._phase1_configure_flathub(dry_run):
                raise Exception("Fáze 1.4 selhala: Flathub konfigurace")
            
            # ========== FÁZE 2: Jádro Systému a CLI Nástroje ==========
            self.logger.info("=" * 60)
            self.logger.info("FÁZE 2: Jádro Systému a CLI Nástroje")
            self.logger.info("=" * 60)
            
            # Fáze 2.2: Setup Docker repository (před instalací balíčků)
            if not self._phase2_setup_docker_repository(dry_run):
                self.logger.warning("Fáze 2.2: Docker repository setup selhal, pokračuji...")
            
            # Fáze 2.1: Instalace jádrových balíčků
            if not self._phase2_install_core_packages(dry_run):
                raise Exception("Fáze 2.1 selhala: Instalace jádrových balíčků")
            
            # Fáze 2.3: Setup ZSH a Oh My Zsh
            if not self._phase2_setup_zsh(dry_run):
                self.logger.warning("Fáze 2.3: ZSH setup selhal, pokračuji...")
            
            # ========== FÁZE 3: Aplikační Vrstva (Flatpak) ==========
            self.logger.info("=" * 60)
            self.logger.info("FÁZE 3: Aplikační Vrstva (Flatpak)")
            self.logger.info("=" * 60)
            
            # Fáze 3.1: Instalace Flatpak aplikací
            if not self._phase3_install_flatpak_apps(dry_run):
                self.logger.warning("Fáze 3.1: Některé Flatpak aplikace selhaly, pokračuji...")
            
            # ========== FÁZE 4: Speciální Instalace ==========
            self.logger.info("=" * 60)
            self.logger.info("FÁZE 4: Speciální Instalace")
            self.logger.info("=" * 60)
            
            # Fáze 4.1: Instalace Micromamba
            if not self._phase4_install_micromamba(dry_run):
                self.logger.warning("Fáze 4.1: Micromamba instalace selhala, pokračuji...")
            
            # Fáze 4.2: Instalace Cursor AppImage
            if not self._phase4_install_cursor_appimage(dry_run):
                self.logger.warning("Fáze 4.2: Cursor AppImage instalace selhala, pokračuji...")
            
            # ========== LEGACY: Konfigurační kroky ==========
            self.logger.info("=" * 60)
            self.logger.info("LEGACY: Dodatečné konfigurační kroky")
            self.logger.info("=" * 60)
            
            # Execute legacy configuration steps
            for step in plan['configuration_steps']:
                self.logger.info(f"Executing legacy step: {step['name']}")

                if step['name'] == 'configure_ssh':
                    self._configure_ssh_server(config, dry_run)
                elif step['name'] == 'setup_tmux':
                    self._setup_tmux_ecosystem(config, dry_run)
                elif step['name'] == 'setup_power_management':
                    self._setup_power_management(config, dry_run)
                elif step['name'] == 'setup_ai_tools':
                    self._setup_ai_tools(config, dry_run)

            self.logger.info("=" * 60)
            self.logger.info("✅ Instalace dokončena úspěšně!")
            self.logger.info("=" * 60)

        except Exception as e:
            self.logger.error(f"Installation failed: {e}")
            raise

    def _configure_ssh_server(self, config: WorkstationConfig, dry_run: bool):
        """Configure SSH server."""
        self.logger.info("Configuring SSH server...")
        ssh_config_path = "/etc/ssh/sshd_config"

        # Idempotency Check
        try:
            with open(ssh_config_path, 'r') as f:
                content = f.read()
            if f"Port {config.ssh_port}" in content:
                self.logger.info(f"SSH port {config.ssh_port} already configured. Skipping.")
                return
        except FileNotFoundError:
            self.logger.error(f"SSH config file not found at {ssh_config_path}")
            raise

        if dry_run:
            self.logger.info(f"Would modify {ssh_config_path} to set Port to {config.ssh_port}")
            self.logger.info("Would restart sshd service.")
            return

        # Replace port configuration
        try:
            # First, try to replace commented port
            subprocess.run(
                ["sudo", "sed", "-i", f"s/^#Port 22/Port {config.ssh_port}/", ssh_config_path],
                check=True
            )
            # If that didn't work, replace uncommented port
            subprocess.run(
                ["sudo", "sed", "-i", f"s/^Port 22/Port {config.ssh_port}/", ssh_config_path],
                check=True
            )
            self.logger.info(f"Successfully updated SSH port to {config.ssh_port} in {ssh_config_path}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to modify SSH config file: {e}")
            raise

        # Restart SSH service
        try:
            self.logger.info("Restarting SSH service...")
            subprocess.run(["sudo", "systemctl", "restart", "sshd"], check=True)
            self.logger.info("SSH service restarted successfully.")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to restart SSH service: {e}")
            # Attempt to revert the change to avoid locking user out
            self.logger.warning("Attempting to revert SSH configuration...")
            subprocess.run(
                ["sudo", "sed", "-i", f"s/^Port {config.ssh_port}/Port 22/", ssh_config_path],
                check=False
            )
            raise


    def _setup_tmux_ecosystem(self, config: WorkstationConfig, dry_run: bool):
        """Setup tmux ecosystem integration by copying the config file and installing tpm."""
        self.logger.info("Setting up tmux ecosystem")

        # 1. Copy tmux.conf
        try:
            script_dir = os.path.dirname(__file__)
            source_path = os.path.join(script_dir, '..', 'configs', 'tmux.conf')
            dest_path = os.path.expanduser("~/.tmux.conf")

            if dry_run:
                self.logger.info(f"Would copy tmux config from {source_path} to {dest_path}")
            else:
                self.logger.info(f"Copying tmux config from {source_path} to {dest_path}")
                shutil.copy(source_path, dest_path)
                self.logger.info("Successfully copied tmux.conf")

        except FileNotFoundError:
            self.logger.error(f"Tmux config source file not found at {source_path}")
            raise
        except Exception as e:
            self.logger.error(f"Failed to copy tmux config: {e}")
            raise

        # 2. Install TPM (Tmux Plugin Manager)
        tpm_path = os.path.expanduser("~/.tmux/plugins/tpm")
        if os.path.exists(tpm_path):
            self.logger.info("TPM already installed. Skipping.")
            return

        if dry_run:
            self.logger.info(f"Would clone TPM into {tpm_path}")
            return

        self.logger.info("Cloning Tmux Plugin Manager (TPM)...")
        try:
            subprocess.run(
                ["git", "clone", "https://github.com/tmux-plugins/tpm", tpm_path],
                check=True,
                capture_output=True,
                text=True
            )
            self.logger.info("TPM cloned successfully.")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to clone TPM: {e.stderr}")
            raise

    def _setup_power_management(self, config: WorkstationConfig, dry_run: bool):
        """Setup Q9550 power management by installing necessary tools."""
        self.logger.info("Setting up Q9550 power management...")
        power_packages = ["cpufrequtils", "lm-sensors"]

        # This step relies on the main package installation logic.
        # We just need to ensure the packages are in the list.
        # The following is for direct invocation or clarity.

        self.logger.info(f"Ensuring packages for power management are installed: {power_packages}")

        # The actual installation is handled by the main `execute_installation` method
        # which gets the list from `create_installation_plan`. We need to add them there.
        # This method is more of a placeholder for future specific logic.

        if dry_run:
            self.logger.info(f"Would ensure {power_packages} are installed.")
            return

        # For now, we can just log that the main installer should handle it.
        self.logger.info("Power management package dependencies are handled by the main installer.")
        self.logger.info("No specific configuration actions are required in this step at this time.")

    def _setup_ai_tools(self, config: WorkstationConfig, dry_run: bool):
        """Setup AI development tools by installing Python packages."""
        self.logger.info("Setting up AI development tools...")

        ai_packages = [
            "openai",
            "anthropic",
            "google-generativeai",
            "torch",
            "transformers",
            "accelerate"
        ]

        for package in ai_packages:
            self.logger.info(f"Checking for Python package: {package}")

            # Idempotency Check
            try:
                result = subprocess.run(["pip", "show", package], capture_output=True, text=True)
                if result.returncode == 0:
                    self.logger.info(f"Package '{package}' already installed. Skipping.")
                    continue
            except FileNotFoundError:
                self.logger.error("'pip' command not found. Cannot install Python packages.")
                raise

            if dry_run:
                self.logger.info(f"Would install Python package: {package}")
                continue

            # Install package
            self.logger.info(f"Installing Python package: {package}...")
            try:
                subprocess.run(["pip", "install", package], check=True, capture_output=True, text=True)
                self.logger.info(f"Successfully installed {package}.")
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Failed to install {package}: {e.stderr}")
                # Continue with other packages

    # ========== FÁZE 1: Základní Systém a Prostředí ==========
    
    def _phase1_update_apt_cache(self, dry_run: bool) -> bool:
        """Fáze 1.1: Aktualizace APT cache."""
        self.logger.info("Fáze 1.1: Aktualizace APT cache...")
        
        if dry_run:
            self.logger.info("Would run: sudo apt update")
            return True
        
        try:
            result = subprocess.run(
                ["sudo", "apt", "update"],
                check=True,
                capture_output=True,
                text=True
            )
            self.logger.info("APT cache úspěšně aktualizována")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Selhala aktualizace APT cache: {e.stderr}")
            return False
    
    def _phase1_install_basic_dependencies(self, dry_run: bool) -> bool:
        """Fáze 1.2: Instalace základních závislostí (flatpak, git)."""
        self.logger.info("Fáze 1.2: Instalace základních závislostí...")
        
        basic_packages = ["flatpak", "git"]
        
        if dry_run:
            self.logger.info(f"Would install: {' '.join(basic_packages)}")
            return True
        
        try:
            # Instalace balíčků
            result = subprocess.run(
                ["sudo", "apt", "install", "-y"] + basic_packages,
                check=True,
                capture_output=True,
                text=True
            )
            self.logger.info("Základní závislosti úspěšně nainstalovány")
            
            # Ověření flatpak
            result = subprocess.run(
                ["flatpak", "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                self.logger.error("Flatpak není dostupný po instalaci")
                return False
            
            self.logger.info(f"Flatpak verze: {result.stdout.strip()}")
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Selhala instalace základních závislostí: {e.stderr}")
            return False
    
    def _phase1_setup_easyflatpak(self, dry_run: bool) -> bool:
        """Fáze 1.3: Nastavení dupotEasyFlatpak."""
        self.logger.info("Fáze 1.3: Nastavení dupotEasyFlatpak...")
        
        easyflatpak_path = self.EASYFLATPAK_DIR
        
        # Kontrola existence adresáře
        if easyflatpak_path.exists():
            self.logger.info(f"dupotEasyFlatpak již existuje v {easyflatpak_path}")
            
            if dry_run:
                self.logger.info(f"Would run: git -C {easyflatpak_path} pull")
                return True
            
            # Aktualizace existujícího repozitáře
            try:
                result = subprocess.run(
                    ["git", "-C", str(easyflatpak_path), "pull"],
                    check=True,
                    capture_output=True,
                    text=True
                )
                self.logger.info("dupotEasyFlatpak úspěšně aktualizován")
                return True
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Selhala aktualizace dupotEasyFlatpak: {e.stderr}")
                return False
        else:
            # Klonování nového repozitáře
            if dry_run:
                self.logger.info(f"Would clone dupotEasyFlatpak to {easyflatpak_path}")
                return True
            
            try:
                # Vytvoření nadřazeného adresáře
                easyflatpak_path.parent.mkdir(parents=True, exist_ok=True)
                
                result = subprocess.run(
                    ["git", "clone", 
                     "https://github.com/imikado/dupotEasyFlatpak.git",
                     str(easyflatpak_path)],
                    check=True,
                    capture_output=True,
                    text=True
                )
                self.logger.info(f"dupotEasyFlatpak úspěšně naklonován do {easyflatpak_path}")
                
                # Ověření existence
                if not easyflatpak_path.exists():
                    self.logger.error("dupotEasyFlatpak adresář neexistuje po klonování")
                    return False
                
                return True
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Selhalo klonování dupotEasyFlatpak: {e.stderr}")
                return False
    
    def _phase1_configure_flathub(self, dry_run: bool) -> bool:
        """Fáze 1.4: Konfigurace Flathub repozitáře."""
        self.logger.info("Fáze 1.4: Konfigurace Flathub repozitáře...")
        
        if dry_run:
            self.logger.info("Would add Flathub remote")
            return True
        
        try:
            # Přidání Flathub repozitáře (pokud ještě není)
            result = subprocess.run(
                ["flatpak", "remote-add", "--if-not-exists", "flathub",
                 "https://flathub.org/repo/flathub.flatpakrepo"],
                check=True,
                capture_output=True,
                text=True
            )
            self.logger.info("Flathub repozitář nakonfigurován")
            
            # Ověření
            result = subprocess.run(
                ["flatpak", "remotes"],
                capture_output=True,
                text=True
            )
            
            if "flathub" in result.stdout:
                self.logger.info("Flathub repozitář úspěšně ověřen")
                return True
            else:
                self.logger.error("Flathub repozitář není v seznamu remotes")
                return False
                
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Selhala konfigurace Flathub: {e.stderr}")
            return False

    # ========== FÁZE 2: Jádro Systému a CLI Nástroje ==========
    
    def _phase2_install_core_packages(self, dry_run: bool) -> bool:
        """Fáze 2.1: Instalace balíčků z APT_CORE_PACKAGES."""
        self.logger.info("Fáze 2.1: Instalace jádrových balíčků...")
        
        if dry_run:
            self.logger.info(f"Would install {len(self.APT_CORE_PACKAGES)} packages")
            return True
        
        try:
            # Sestavení příkazu
            cmd = ["sudo", "apt", "install", "-y"] + self.APT_CORE_PACKAGES
            
            self.logger.info(f"Instaluji {len(self.APT_CORE_PACKAGES)} balíčků...")
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )
            self.logger.info("Jádrové balíčky úspěšně nainstalovány")
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Selhala instalace jádrových balíčků: {e.stderr}")
            return False
    
    def _phase2_setup_docker_repository(self, dry_run: bool) -> bool:
        """Fáze 2.2: Zajištění repozitáře pro Docker."""
        self.logger.info("Fáze 2.2: Nastavení Docker repozitáře...")
        
        docker_list_path = "/etc/apt/sources.list.d/docker.list"
        
        # Kontrola existence
        if os.path.exists(docker_list_path):
            self.logger.info("Docker repozitář již existuje")
            return True
        
        if dry_run:
            self.logger.info("Would setup Docker repository")
            return True
        
        try:
            # Přidání GPG klíče
            self.logger.info("Přidávám Docker GPG klíč...")
            subprocess.run(
                ["sudo", "mkdir", "-p", "/etc/apt/keyrings"],
                check=True
            )
            
            # Stažení a instalace GPG klíče
            subprocess.run(
                "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | "
                "sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg",
                shell=True,
                check=True
            )
            
            # Přidání repozitáře
            self.logger.info("Přidávám Docker repozitář...")
            subprocess.run(
                'echo "deb [arch=$(dpkg --print-architecture) '
                'signed-by=/etc/apt/keyrings/docker.gpg] '
                'https://download.docker.com/linux/ubuntu '
                '$(lsb_release -cs) stable" | '
                'sudo tee /etc/apt/sources.list.d/docker.list > /dev/null',
                shell=True,
                check=True
            )
            
            # Aktualizace APT cache
            subprocess.run(
                ["sudo", "apt", "update"],
                check=True,
                capture_output=True
            )
            
            self.logger.info("Docker repozitář úspěšně nakonfigurován")
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Selhalo nastavení Docker repozitáře: {e}")
            return False
    
    def _phase2_setup_zsh(self, dry_run: bool) -> bool:
        """Fáze 2.3: Nastavení ZSH a Oh My Zsh."""
        self.logger.info("Fáze 2.3: Nastavení ZSH a Oh My Zsh...")
        
        oh_my_zsh_path = Path.home() / ".oh-my-zsh"
        
        # Kontrola existence Oh My Zsh
        if oh_my_zsh_path.exists():
            self.logger.info("Oh My Zsh již je nainstalován")
            return True
        
        if dry_run:
            self.logger.info("Would install Oh My Zsh")
            return True
        
        try:
            # Upozornění uživatele
            self.logger.warning("Instalace Oh My Zsh může vyžadovat interakci uživatele")
            
            # Neinteraktivní instalace Oh My Zsh
            install_script = (
                'sh -c "$(curl -fsSL '
                'https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" '
                '"" --unattended'
            )
            
            result = subprocess.run(
                install_script,
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            
            # Ověření instalace
            if not oh_my_zsh_path.exists():
                self.logger.error("Oh My Zsh nebyl nainstalován")
                return False
            
            self.logger.info("Oh My Zsh úspěšně nainstalován")
            
            # Nastavení ZSH jako výchozí shell
            try:
                subprocess.run(
                    ["chsh", "-s", "/usr/bin/zsh"],
                    check=True,
                    capture_output=True
                )
                self.logger.info("ZSH nastaven jako výchozí shell")
            except subprocess.CalledProcessError:
                self.logger.warning("Nepodařilo se nastavit ZSH jako výchozí shell")
            
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Selhala instalace Oh My Zsh: {e}")
            return False

    # ========== FÁZE 3: Aplikační Vrstva (Flatpak) ==========
    
    def _phase3_install_flatpak_apps(self, dry_run: bool) -> bool:
        """Fáze 3.1: Instalace Flatpak aplikací přes easy-flatpak."""
        self.logger.info("Fáze 3.1: Instalace Flatpak aplikací...")
        
        easyflatpak_script = self.EASYFLATPAK_DIR / "easy-flatpak.sh"
        
        # Kontrola existence skriptu
        if not easyflatpak_script.exists():
            self.logger.error(f"easy-flatpak.sh nenalezen v {easyflatpak_script}")
            return False
        
        success_count = 0
        failed_apps = []
        
        for app in self.FLATPAK_APPS:
            self.logger.info(f"Instaluji aplikaci: {app}")
            
            if dry_run:
                self.logger.info(f"Would install: {app}")
                success_count += 1
                continue
            
            try:
                # Spuštění easy-flatpak.sh install
                cmd = [str(easyflatpak_script), "install", app]
                result = subprocess.run(
                    cmd,
                    check=True,
                    capture_output=True,
                    text=True
                )
                
                self.logger.info(f"✓ {app} úspěšně nainstalován")
                success_count += 1
                
            except subprocess.CalledProcessError as e:
                self.logger.error(f"✗ Selhala instalace {app}: {e.stderr}")
                failed_apps.append(app)
                # Pokračujeme s dalšími aplikacemi
        
        # Souhrn
        self.logger.info(f"Instalace dokončena: {success_count}/{len(self.FLATPAK_APPS)} úspěšných")
        
        if failed_apps:
            self.logger.warning(f"Selhaly aplikace: {', '.join(failed_apps)}")
            return False
        
        return True

    # ========== FÁZE 4: Speciální Instalace ==========
    
    def _phase4_install_micromamba(self, dry_run: bool) -> bool:
        """Fáze 4.1: Instalace Micromamba."""
        self.logger.info("Fáze 4.1: Instalace Micromamba...")
        
        # Kontrola existence
        try:
            result = subprocess.run(
                ["command", "-v", "micromamba"],
                shell=True,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                self.logger.info("Micromamba již je nainstalován")
                return True
        except:
            pass
        
        if dry_run:
            self.logger.info("Would install Micromamba")
            return True
        
        try:
            self.logger.warning("Instalace Micromamba může být interaktivní")
            
            # Instalace přes oficiální skript
            install_cmd = "bash <(curl -L micro.mamba.pm/install.sh)"
            result = subprocess.run(
                install_cmd,
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            
            # Ověření instalace
            result = subprocess.run(
                ["command", "-v", "micromamba"],
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.logger.info("Micromamba úspěšně nainstalován")
                return True
            else:
                self.logger.error("Micromamba nebyl nalezen po instalaci")
                return False
                
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Selhala instalace Micromamba: {e}")
            return False
    
    def _phase4_install_cursor_appimage(self, dry_run: bool) -> bool:
        """Fáze 4.2: Instalace Cursor AppImage."""
        self.logger.info("Fáze 4.2: Instalace Cursor AppImage...")
        
        # URL pro Cursor AppImage (nejnovější verze)
        cursor_url = "https://downloader.cursor.sh/linux/appImage/x64"
        cursor_path = self.APPIMAGE_DIR / "Cursor.AppImage"
        
        # Kontrola existence
        if cursor_path.exists():
            self.logger.info(f"Cursor AppImage již existuje v {cursor_path}")
            return True
        
        if dry_run:
            self.logger.info(f"Would download Cursor to {cursor_path}")
            return True
        
        try:
            # Vytvoření adresáře pro AppImages
            self.APPIMAGE_DIR.mkdir(parents=True, exist_ok=True)
            
            # Stažení Cursor AppImage
            self.logger.info(f"Stahuji Cursor z {cursor_url}...")
            result = subprocess.run(
                ["wget", "-O", str(cursor_path), cursor_url],
                check=True,
                capture_output=True,
                text=True
            )
            
            # Ověření existence souboru
            if not cursor_path.exists():
                self.logger.error("Cursor AppImage nebyl stažen")
                return False
            
            # Nastavení oprávnění ke spuštění
            self.logger.info("Nastavuji oprávnění ke spuštění...")
            subprocess.run(
                ["chmod", "+x", str(cursor_path)],
                check=True
            )
            
            # Ověření oprávnění
            if not os.access(cursor_path, os.X_OK):
                self.logger.error("Cursor AppImage nemá oprávnění ke spuštění")
                return False
            
            self.logger.info(f"Cursor AppImage úspěšně nainstalován do {cursor_path}")
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Selhala instalace Cursor AppImage: {e}")
            return False

    def validate_installation(self) -> bool:
        """Validate completed installation."""
        self.logger.info("Validating installation")

        validation_report = self.config_validator.generate_validation_report()

        if validation_report.overall_status == "error":
            self.logger.error("Installation validation failed")
            for issue in validation_report.critical_issues:
                self.logger.error(f"Critical issue: {issue}")
            return False
        else:
            self.logger.info("Installation validation passed")
            return True

    def run_setup(self, dry_run: bool = False):
        """Main setup workflow."""
        try:
            # Welcome message
            if self.language == "cz":
                print("🚀 Vítejte v Unification Workstation Setup")
                print("Inteligentní automatizace nastavení vývojové stanice")
            else:
                print("🚀 Welcome to Unification Workstation Setup")
                print("Intelligent development workstation automation")

            # Gather requirements
            config = self.gather_requirements(dry_run=dry_run)

            # Analyze system
            analysis = self.analyze_system()

            # Create installation plan
            plan = self.create_installation_plan(config, analysis)

            # Display plan
            self.display_installation_plan(plan)

            # Confirm execution
            if not dry_run:
                try:
                    if self.language == "cz":
                        confirm_prompt = "\nPokračovat s instalací? (y/n): "
                        confirm = input(confirm_prompt).lower()
                    else:
                        confirm_prompt = "\nProceed with installation? (y/n): "
                        confirm = input(confirm_prompt).lower()

                    if confirm not in ['y', 'yes', 'ano']:
                        print("Installation cancelled / Instalace zrušena")
                        return
                except EOFError:
                    # If no input available, proceed with installation
                    if self.language == "cz":
                        print("\n⚠️  Žádný vstup - pokračuji s instalací...")
                    else:
                        print("\n⚠️  No input - proceeding with installation...")
            else:
                if self.language == "cz":
                    print("\n🔍 DRY RUN - Simulace instalace...")
                else:
                    print("\n🔍 DRY RUN - Simulating installation...")

            # Execute installation
            self.execute_installation(plan, config, dry_run=dry_run)

            # Validate installation
            if self.validate_installation():
                if self.language == "cz":
                    print("\n✅ Workstation setup dokončen úspěšně!")
                else:
                    print("\n✅ Workstation setup completed successfully!")
            else:
                if self.language == "cz":
                    print("\n❌ Setup dokončen s chybami. Zkontrolujte logy.")
                else:
                    print("\n❌ Setup completed with errors. Check logs.")

        except KeyboardInterrupt:
            print("\n\nSetup cancelled by user / Setup zrušen uživatelem")
        except Exception as e:
            self.logger.error(f"Setup failed: {e}")
            if self.language == "cz":
                print(f"\n❌ Setup selhal: {e}")
            else:
                print(f"\n❌ Setup failed: {e}")


if __name__ == "__main__":
    wizard = WorkstationWizard()
    wizard.run_setup()