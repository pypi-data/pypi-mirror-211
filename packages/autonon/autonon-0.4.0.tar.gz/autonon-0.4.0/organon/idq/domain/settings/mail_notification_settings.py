"""Includes MailNotificationSettings class."""
from typing import List


class MailNotificationSettings:
    """"Settings for mail notification."""
    def __init__(self):
        self.addresses: List[str] = None
        self.cc_addresses: List[str] = None
