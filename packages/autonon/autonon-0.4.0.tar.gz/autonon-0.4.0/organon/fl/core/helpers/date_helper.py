"""
This module keeps the helper functions for datetime type.
"""
from datetime import datetime, timedelta
from typing import Union

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

from organon.fl.core.helpers.string_helper import is_null_or_empty


def now() -> datetime:
    """
    Returns the current(now) time as a datetime.
    :return: current time
    """
    return datetime.now()


def format_date(date: datetime, format_str: str = None) -> str:
    """
    Formats and returns the date as a string.
    :param date: datetime object to be formatted
    :param format_str: datetime format string
    :return: string representation of the date
    """
    if format_str is None:
        format_str = "%Y-%m-%d %H:%M:%S"
        return date.strftime(format_str)
    return date.strftime(format_str)


def get_date_from_string(date_string: str, date_format: str = "", iso_format: bool = False) -> datetime:
    """
    Converts a date written as string to datetime
    :param date_string: A date written as string
    :type date_string: str
    :param date_format: Format of the date_string
    :type date_format: str
    :param iso_format: specifies is given date string is in iso format
    :type iso_format bool
    :return: datetime instance with given date
    """
    if is_null_or_empty(date_format):
        if iso_format:
            return datetime.fromisoformat(date_string)
        return parse(date_string)
    return datetime.strptime(date_string, date_format)


# pylint: disable=too-many-arguments
def add_to_date(date: datetime, years: int = 0, months: int = 0, days: int = 0, hours: int = 0,
                minutes: int = 0, seconds: int = 0, milliseconds: int = 0, microseconds: int = 0,
                delta: Union[timedelta, relativedelta] = None) -> datetime:
    """
    Adds given values (1 year, 2 seconds etc., -2 months) to given date
    :param microseconds:
    :param milliseconds:
    :param seconds:
    :param hours:
    :param days:
    :param months:
    :param years:
    :param minutes:
    :param date: Initial date
    :param delta: timedelta or relativedelta to add to date
    :return: Date after addition
    """
    if delta is None:
        delta = get_time_delta(years, months, days, hours, minutes, seconds, milliseconds, microseconds)
    return date + delta


def get_time_delta(years: int = 0, months: int = 0, days: int = 0, hours: int = 0,
                   minutes: int = 0, seconds: int = 0, milliseconds: int = 0,
                   microseconds: int = 0) -> relativedelta or timedelta:
    """Returns a timedelta/relativedelta object according to given date delta values.
    The returned obejct can be used to add a timedelta to a datetime object."""
    if milliseconds != 0:
        microseconds += milliseconds * 1000
    if years == 0 and months == 0:
        delta = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds,
                          microseconds=microseconds)
    else:
        delta = relativedelta(years=years, months=months, days=days, hours=hours, minutes=minutes, seconds=seconds,
                              microseconds=microseconds)
    return delta


def date_to_milliseconds(date: datetime) -> int:
    """
    Converts a datetime instance to milliseconds
    :param date: date to be converted
    :type date: datetime
    :return: milliseconds
    """
    epoch = datetime.utcfromtimestamp(0)
    return int((date - epoch).total_seconds() * 1000)


def milliseconds_to_date(milliseconds: int) -> datetime:
    """
    Converts milliseconds to datetime
    :param int milliseconds: milliseconds since 01-01-1970 (utc)
    :return: milliseconds
    """
    microseconds = int(milliseconds) * 1000  # convert to int to support numpy.int as argument
    epoch = datetime.utcfromtimestamp(0)
    date = epoch + timedelta(microseconds=microseconds)
    return date


class DateDifference:
    """Stores date difference info"""

    def __init__(self, seconds):
        self.total_seconds = seconds
        self.total_minutes = self.total_seconds / 60
        self.total_hours = self.total_minutes / 60
        self.total_days = self.total_hours / 24


def get_date_difference(date1: datetime, date2: datetime):
    """Returns date difference"""
    return DateDifference((date1 - date2).total_seconds())


def get_date_as_integer(date: datetime) -> int:
    """Returns number of milliseconds since 01.01.1970 to given date"""
    try:
        return date_to_milliseconds(date)
    except Exception as exc:  # pylint: disable=broad-except
        raise ValueError(f"Date {format_date(date)} cannot be converted to integer") from exc


def get_integer_as_date(num_milliseconds: int) -> datetime:
    """Converts given number of milliseconds to datetime
    :param int num_milliseconds: number of milliseconds since 01.01.1970 to given date
    """
    try:
        return milliseconds_to_date(num_milliseconds)
    except Exception as exc:  # pylint: disable=broad-except
        raise ValueError(f"Integer {num_milliseconds} cannot be converted to datetime") from exc
