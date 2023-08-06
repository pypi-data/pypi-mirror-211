"""Includes DqNotificationSettings class."""
from organon.idq.domain.settings.mail_notification_settings import MailNotificationSettings


class DqNotificationSettings:
    """Notification settings for DQ execution."""
    def __init__(self):
        self.mail_notification_settings: MailNotificationSettings = None
