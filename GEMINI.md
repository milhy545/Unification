# Gemini Project: Unification - System Setup Automation

## 🚀 Project Overview

Unification is a sophisticated automation framework written in Python for setting up and managing multi-server development environments. The project aims to solve the complexities of system administration through intelligent automation, with a focus on reproducibility and consistency.

The framework is designed to be modular and extensible, with a `master_wizard.py` script acting as the main entry point. This script presents a menu of setup scenarios, and based on the user's choice, it dynamically loads and executes the corresponding "wizard" module from the `wizards/` directory.

The project also includes a suite of powerful tools in the `tools/` directory that provide functionalities such as:

*   **System Detection:** Gathering comprehensive information about the hardware, OS, and software of a machine.
*   **Dependency Resolution:** Abstracting package management across different Linux distributions.
*   **Network Scanning:** Discovering the network topology and identifying services running on different servers.
*   **Configuration Validation:** Checking the integrity and correctness of various configuration files.

The project is well-documented, with bilingual support for English and Czech.

## 🏗️ Building and Running

To run the Unification framework, simply execute the `master_wizard.py` script using Python 3:

```bash
python3 master_wizard.py
```

You can also run a specific setup scenario directly by using the `--scenario` flag:

```bash
python3 master_wizard.py --scenario workstation
```

## 💻 Development Conventions

*   **Language:** The project is written in Python 3.
*   **Style:** The code follows the PEP 8 style guide.
*   **Typing:** The project uses type hints for better code clarity and maintainability.
*   **Modularity:** The code is organized into modules with specific responsibilities (wizards, tools).
*   **Logging:** The project uses the `logging` module to provide detailed information about the execution flow.
*   **Bilingual Support:** User-facing strings are provided in both English and Czech.

## 🌐 Ecosystem Overview

The Unification framework is designed to manage a multi-server development ecosystem. The `GEMINI_MEMORY_BRIEFING.md` file provides a detailed overview of this ecosystem, which consists of three main machines:

1.  **WORKSTATION (Aspire-PC):** The primary development and testing machine.
2.  **LLM SERVER (LLMS):** A dedicated server for AI processing and running large language models.
3.  **AUTOMATION HUB (HAS):** An orchestration hub that runs the ZEN Coordinator and other core services.

The `GEMINI_MEMORY_BRIEFING.md` file contains critical information about the architecture, SSH access, critical services, and safety rules for each machine. It is essential to consult this document before performing any operations on the ecosystem.
