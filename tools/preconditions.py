"""
Preconditions utility
Lightweight checks for environment and system capabilities used across wizards.
"""

import os
import shutil
import socket
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def has_command(cmd: str) -> bool:
    """Return True if command is available in PATH.
    Uses shutil.which and logs at debug level.
    """
    path = shutil.which(cmd)
    available = path is not None
    logger.debug("has_command('%s') -> %s (path=%s)", cmd, available, path)
    return available


def is_root_or_sudo() -> bool:
    """Return True if running as root or via sudo (uid 0)."""
    try:
        return os.geteuid() == 0  # type: ignore[attr-defined]
    except Exception:
        # Fallback for non-posix platforms
        return os.name == 'nt' and 'PROGRAMW6432' in os.environ


def has_network(timeout: float = 2.0) -> bool:
    """Best-effort network connectivity check using DNS and TCP.
    Attempts to resolve and connect to a known host (8.8.8.8:53)."""
    try:
        with socket.create_connection(("8.8.8.8", 53), timeout=timeout):
            return True
    except OSError as e:
        logger.info("Network check failed: %s", e)
        return False


def explain_environment() -> dict:
    """Provide a tiny snapshot of environment useful for logs and dry-runs."""
    info = {
        "is_root": is_root_or_sudo(),
        "has_ip": has_command("ip"),
        "has_flatpak": has_command("flatpak"),
        "has_apt": has_command("apt"),
        "has_pacman": has_command("pacman"),
        "has_apk": has_command("apk"),
        "network": has_network(),
    }
    logger.debug("Environment: %s", info)
    return info
