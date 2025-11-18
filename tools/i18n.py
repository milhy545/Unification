"""
Minimal i18n helper for bilingual messages (en/cz).
Use i18n.get(key, lang, default) to fetch localized strings.
"""
from typing import Dict

_MESSAGES: Dict[str, Dict[str, str]] = {
    "banner_title": {
        "en": "UNIFICATION SYSTEM SETUP",
        "cz": "UNIFIKACE NASTAVENÍ SYSTÉMU",
    },
    "prompt_select_option": {
        "en": "Select an option:",
        "cz": "Vyberte možnost:",
    },
    "info_env_summary": {
        "en": "Environment summary",
        "cz": "Souhrn prostředí",
    },
}


def get(key: str, lang: str = "en", default: str = "") -> str:
    """Return localized message, or default if not available."""
    return _MESSAGES.get(key, {}).get(lang, default or key)
