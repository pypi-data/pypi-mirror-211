"""Includes DateValueDefinition class."""
from typing import List

from organon.fl.core.enums.datetime_token import DatetimeToken


class DateValueDefinition:
    """Date value definition class."""

    def __init__(self, year: int = None, month: int = None, day: int = None, hour: int = None):
        self.year: int = year
        self.month: int = month
        self.day: int = day
        self.hour: int = hour

    def get_datetime_tokens(self) -> List[DatetimeToken]:
        """Returns tokens for supplied values in date value definition"""
        tokens = []
        if self.year is not None:
            tokens.append(DatetimeToken.YEAR)
        if self.month is not None:
            tokens.append(DatetimeToken.MONTH)
        if self.day is not None:
            tokens.append(DatetimeToken.DAY)
        if self.hour is not None:
            tokens.append(DatetimeToken.HOUR)
        return tokens
