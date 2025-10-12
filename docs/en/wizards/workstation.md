# Workstation Setup Wizard

The Workstation Setup Wizard is a key component of the Unification framework, designed to automate the complete setup of a development workstation, specifically tailored for the "Aspire-PC" type machine.

## Overview

This wizard guides the user through a series of questions to configure a new development environment from scratch. It handles package installation, service configuration, and setup of specialized development tools. The entire process is designed to be **idempotent**, meaning it can be run multiple times on the same system without causing errors or duplicate configurations.

## Features

The wizard automates the following setup stages:

1.  **Requirement Gathering:** Interactively asks the user what components to install and configure.
2.  **System Analysis:** Detects the current OS, hardware (including special detection for the Q9550 CPU), and network state.
3.  **Plan Creation:** Generates a detailed installation plan, estimating the time and disk space required.
4.  **Execution:** Performs the actual system modifications.
5.  **Validation:** Checks that all configurations were applied correctly.

### Detailed Actions

-   **Package Installation:**
    -   Installs a base set of required packages (`git`, `python3`, `ssh`, `tmux`, etc.).
    -   Optionally installs a full suite of development tools (`docker`, `code`, `build-essential`, etc.).
    -   Optionally installs packages required for power management on Q9550 CPUs (`cpufrequtils`, `lm-sensors`).

-   **SSH Server Configuration:**
    -   Configures the SSH server to run on port `2222`.
    -   Disables root login for enhanced security.
    -   Ensures the service is enabled and running.

-   **Tmux Ecosystem Setup:**
    -   Copies the standard `.tmux.conf` configuration file to the user's home directory.
    -   Clones the Tmux Plugin Manager (TPM) repository to `~/.tmux/plugins/tpm` if it doesn't exist, preparing it for use.

-   **AI Tools Setup:**
    -   Installs a predefined list of essential Python packages for AI development via `pip`, including:
        -   `openai`
        -   `anthropic`
        -   `google-generativeai`
        -   `torch`
        -   `transformers`
        -   `accelerate`

## How to Run

The wizard can be run directly via the `master_wizard.py` script:

```bash
# Run in interactive mode and select from the menu
python3 master_wizard.py

# Run the workstation scenario directly
python3 master_wizard.py --scenario workstation

# Perform a dry run without making any system changes
python3 master_wizard.py --scenario workstation --dry-run
```
