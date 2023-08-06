"""Includes helper functions for afe date columns."""
from datetime import timedelta, datetime
from typing import Callable

from organon.afe.domain.enums.afe_date_column_type import AfeDateColumnType
from organon.afe.domain.enums.date_resolution import DateResolution
from organon.fl.core.helpers.date_helper import get_date_from_string, format_date


def get_date_subtraction_func(resolution: DateResolution, delta_value: int) -> Callable[[int], int]:
    """
    Returns a function to manipulate a date based on given resolution
    :param resolution:
    :type resolution: DateResolution
    :param delta_value: number of years,month,dates.. to add as delta
    :type delta_value: int
    :return: Function to manipulate date
    """
    step = -1 * delta_value

    function_map = {
        DateResolution.Year: timedelta(days=365 * step).total_seconds(),
        DateResolution.Month: timedelta(days=30 * step).total_seconds(),
        DateResolution.Day: timedelta(days=step).total_seconds(),  # timedelta is faster
        DateResolution.Hour: timedelta(hours=step).total_seconds(),
        DateResolution.Minute: timedelta(minutes=step).total_seconds(),
        DateResolution.Second: timedelta(seconds=step).total_seconds()
    }
    if resolution in function_map:
        delta = int(function_map[resolution] * 1000)
        return lambda timestamp: timestamp + delta

    raise NotImplementedError


def get_str_to_date_converter(date_column_type: AfeDateColumnType, date_custom_format: str = None) -> \
        Callable[[str], datetime]:
    """
    Returns a function that performs string to date conversion according to date column type and if necessary
    date custom format
    """
    if date_column_type == AfeDateColumnType.DateTime:
        return lambda s: get_date_from_string(s, iso_format=True)
    if date_column_type == AfeDateColumnType.YyyyMmDd:
        return lambda s: datetime(int(s[0:4]), int(s[4:6]), int(s[6:8]))
    if date_column_type == AfeDateColumnType.YyyyMm:
        return lambda s: datetime(int(s[0:4]), int(s[4:6]), 1)
    if date_column_type == AfeDateColumnType.CustomFormat:
        return lambda s: get_date_from_string(s, date_custom_format)
    raise NotImplementedError


def get_date_to_str_converter(date_column_type: AfeDateColumnType, date_custom_format: str = None) -> Callable[
    [datetime], str]:
    """Returns a function that will convert a given datetime object to string according to date_column_type"""
    if date_column_type == AfeDateColumnType.DateTime:
        return lambda s: format_date(s)  # pylint: disable=unnecessary-lambda
    if date_column_type == AfeDateColumnType.YyyyMmDd:
        return lambda s: format_date(s, "%Y%m%d")
    if date_column_type == AfeDateColumnType.YyyyMm:
        return lambda s: format_date(s, "%Y%m")
    if date_column_type == AfeDateColumnType.CustomFormat:
        return lambda s: format_date(s, date_custom_format)
    raise NotImplementedError
