"""
This module keeps the helper functions for double type.
"""
import decimal
import math
from decimal import Decimal

from organon.fl.mathematics.constants import DOUBLE_MAX, DOUBLE_MIN


def round_value(value: float, places: int) -> float:
    """
    Rounds the value.
    :param value: float value to be rounded
    :param places: decimal points
    :return: rounded float value
    """
    if places < 0:
        raise ValueError
    decimal_value = Decimal(value)
    decimal_value = decimal_value.quantize(Decimal('0.' + places * '0'), rounding=decimal.ROUND_HALF_UP)
    return float(decimal_value)


def is_extreme(value: float) -> bool:
    """Returns true if value has an extreme value like nan ,infinity etc."""
    if math.isnan(value) or value == float("inf") or value == float("-inf") or value <= DOUBLE_MIN \
            or value >= DOUBLE_MAX:
        return True
    return False


def equals(val1: float, val2: float):
    """Returns true if both vals equal or both nan"""
    if math.isnan(val1):
        return math.isnan(val2)
    return val1 == val2
