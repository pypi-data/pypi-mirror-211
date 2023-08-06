"""
This module includes BaseAfeSettings class.
"""
from organon.afe.domain.settings.afe_process_settings import AfeProcessSettings


class BaseAfeSettings:
    """Base class for afe modelling/scoring settings"""

    def __init__(self):
        self.process_settings: AfeProcessSettings = None
