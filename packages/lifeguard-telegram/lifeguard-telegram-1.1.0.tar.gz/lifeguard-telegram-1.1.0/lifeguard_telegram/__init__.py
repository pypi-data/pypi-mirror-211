"""
Lifeguard integration with Telegram
"""
import os

from lifeguard.notifications import append_notification_implementation
from lifeguard.logger import lifeguard_logger as logger

from lifeguard_telegram.bot import init_updater
from lifeguard_telegram.notifications import TelegramNotificationBase


class LifeguardTelegramPlugin:
    """
    Telegram Plugin
    """

    def __init__(self, lifeguard_context):
        self.lifeguard_context = lifeguard_context
        init_updater()


def init(lifeguard_context):
    append_notification_implementation(TelegramNotificationBase)
    newpid = os.fork()
    if newpid == 0:
        logger.info("starting telegram process")
        LifeguardTelegramPlugin(lifeguard_context)
