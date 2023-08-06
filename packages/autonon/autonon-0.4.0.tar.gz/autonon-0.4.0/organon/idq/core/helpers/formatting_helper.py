"""Includes FormattingHelper class."""
from organon.fl.core.helpers import float_helper


class FormattingHelper:
    """Includes helper methods for value formatting"""

    @staticmethod
    def to_nullable(value: float):
        """Return None if value is an extreme float value, else return value as it is"""
        if float_helper.is_extreme(value):
            return None
        return value
