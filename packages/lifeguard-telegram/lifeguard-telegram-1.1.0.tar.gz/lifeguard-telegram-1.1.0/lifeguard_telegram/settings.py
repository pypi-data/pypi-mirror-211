"""
Lifeguard Telegram Settings
"""
from lifeguard.settings import SettingsManager

SETTINGS_MANAGER = SettingsManager(
    {
        "LIFEGUARD_TELEGRAM_VALIDATIONS_HANDLER": {
            "default": "true",
            "description": "Enable telegram validations handler",
        },
        "TELEGRAM_API_KEY": {
            "default": "",
            "description": "Telegram bot token",
        },
        "TELEGRAM_DEFAULT_CHAT_ID": {
            "default": "",
            "description": "Telegram default chat id",
        },
    }
)

LIFEGUARD_TELEGRAM_VALIDATIONS_HANDLER_ENABLED = (
    SETTINGS_MANAGER.read_value("LIFEGUARD_TELEGRAM_VALIDATIONS_HANDLER_ENABLED")
    == "true"
)
TELEGRAM_API_KEY = SETTINGS_MANAGER.read_value("TELEGRAM_API_KEY")
TELEGRAM_DEFAULT_CHAT_ID = SETTINGS_MANAGER.read_value("TELEGRAM_DEFAULT_CHAT_ID")
