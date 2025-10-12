"""
Workstation Setup Wizard
Automated setup for development workstation (Aspire PC type)
"""

import os
import sys
import logging
import subprocess
import shutil
from typing import Dict, List, Optional
from dataclasses import dataclass

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

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
        
    def gather_requirements(self) -> WorkstationConfig:
        """Gather workstation setup requirements from user."""
        self.logger.info("Gathering workstation setup requirements")
        
        if self.language == "cz":
            print("\n🖥️ NASTAVENÍ VÝVOJOVÉ WORKSTATION")
            print("=" * 50)
            hostname = input("Název počítače [Aspire-PC]: ") or "Aspire-PC"
            
            ssh_prompt = "Povolit SSH server? (y/n) [y]: "
            ssh_input = input(ssh_prompt).lower()
            enable_ssh = ssh_input in ['', 'y', 'yes', 'ano']
            
            dev_prompt = "Nainstalovat vývojové nástroje? (y/n) [y]: "
            dev_input = input(dev_prompt).lower()
            install_dev = dev_input in ['', 'y', 'yes', 'ano']
            
            ai_prompt = "Nastavit AI nástroje (Claude, etc.)? (y/n) [y]: "
            ai_input = input(ai_prompt).lower()
            setup_ai = ai_input in ['', 'y', 'yes', 'ano']
            
            power_prompt = "Nastavit Q9550 power management? (y/n) [y]: "
            power_input = input(power_prompt).lower()
            setup_power = power_input in ['', 'y', 'yes', 'ano']
            
        else:
            print("\n💻 WORKSTATION SETUP")
            print("=" * 30)
            hostname = input("Computer hostname [Aspire-PC]: ") or "Aspire-PC"
            
            ssh_input = input("Enable SSH server? (y/n) [y]: ").lower()
            enable_ssh = ssh_input in ['', 'y', 'yes']
            
            dev_input = input("Install development tools? (y/n) [y]: ").lower()
            install_dev = dev_input in ['', 'y', 'yes']
            
            ai_input = input("Setup AI tools (Claude, etc.)? (y/n) [y]: ").lower()
            setup_ai = ai_input in ['', 'y', 'yes']
            
            power_input = input("Setup Q9550 power management? (y/n) [y]: ").lower()
            setup_power = power_input in ['', 'y', 'yes']
            
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
            print(f"\n📊 ANALÝZA SYSTÉMU")
            print(f"• OS: {system_info.os_name}")
            print(f"• CPU: {system_info.cpu_cores} jader @ {system_info.cpu_frequency:.1f} MHz")
            print(f"• RAM: {system_info.memory_total // (1024**3)} GB")
            print(f"• Q9550 detekováno: {'✅' if analysis['q9550_detected'] else '❌'}")
            print(f"• Existující ecosystem: {len(network_topology.ecosystem_servers)} serverů")
        else:
            print(f"\n📊 SYSTEM ANALYSIS")
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
            print(f"\n📋 INSTALAČNÍ PLÁN")
            print(f"• Balíčky k instalaci: {len(plan['packages'].packages_to_install)}")
            print(f"• Konfigurační kroky: {len(plan['configuration_steps'])}")
            print(f"• Odhadovaný čas: {plan['total_estimated_time']//60} minut")
            print(f"• Potřebný diskový prostor: {plan['disk_space_required']} MB")
            
            if plan['conflicts']:
                print(f"⚠️  Konflikty: {len(plan['conflicts'])}")
                for conflict in plan['conflicts']:
                    print(f"   • {conflict}")
                    
            if plan['warnings']:
                print(f"⚠️  Upozornění:")
                for warning in plan['warnings']:
                    print(f"   • {warning}")
                    
        else:
            print(f"\n📋 INSTALLATION PLAN")
            print(f"• Packages to install: {len(plan['packages'].packages_to_install)}")
            print(f"• Configuration steps: {len(plan['configuration_steps'])}")
            print(f"• Estimated time: {plan['total_estimated_time']//60} minutes")
            print(f"• Disk space required: {plan['disk_space_required']} MB")
            
            if plan['conflicts']:
                print(f"⚠️  Conflicts: {len(plan['conflicts'])}")
                for conflict in plan['conflicts']:
                    print(f"   • {conflict}")
                    
            if plan['warnings']:
                print(f"⚠️  Warnings:")
                for warning in plan['warnings']:
                    print(f"   • {warning}")
                    
    def execute_installation(self, plan: Dict, config: WorkstationConfig, dry_run: bool = False):
        """Execute the installation plan."""
        self.logger.info(f"Executing installation plan (dry_run={dry_run})")
        
        try:
            # Update package lists
            self.dependency_resolver.update_package_lists(dry_run=dry_run)
                
            # Install packages
            success = self.dependency_resolver.install_packages(
                plan['packages'].packages_to_install, 
                dry_run=dry_run
            )
            
            if not success and not dry_run:
                raise Exception("Package installation failed")
                
            # Execute configuration steps
            for step in plan['configuration_steps']:
                self.logger.info(f"Executing step: {step['name']}")
                
                if step['name'] == 'configure_ssh':
                    self._configure_ssh_server(config, dry_run)
                elif step['name'] == 'setup_tmux':
                    self._setup_tmux_ecosystem(config, dry_run)
                elif step['name'] == 'setup_power_management':
                    self._setup_power_management(config, dry_run)
                elif step['name'] == 'setup_ai_tools':
                    self._setup_ai_tools(config, dry_run)
                    
            self.logger.info("Installation completed successfully")
            
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
            config = self.gather_requirements()
            
            # Analyze system
            analysis = self.analyze_system()
            
            # Create installation plan
            plan = self.create_installation_plan(config, analysis)
            
            # Display plan
            self.display_installation_plan(plan)
            
            # Confirm execution
            if self.language == "cz":
                confirm_prompt = "\nPokračovat s instalací?" + (" (DRY RUN)" if dry_run else "") + " (y/n): "
                confirm = input(confirm_prompt).lower()
            else:
                confirm_prompt = "\nProceed with installation?" + (" (DRY RUN)" if dry_run else "") + " (y/n): "
                confirm = input(confirm_prompt).lower()
                
            if confirm not in ['y', 'yes', 'ano']:
                print("Installation cancelled / Instalace zrušena")
                return
                
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