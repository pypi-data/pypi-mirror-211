"""This module includes "Interval" class."""
import functools

from organon.fl.core.exceptionhandling.known_exception import KnownException
from organon.fl.mathematics.enums.sets.interval_type import IntervalType


@functools.total_ordering
class Interval:
    """Class for Interval"""

    def __init__(self, interval_id: str, lower_bound: float, upper_bound: float, interval_type: IntervalType):
        self.__interval_id: str = interval_id
        self.__lower_bound: float = lower_bound
        self.__upper_bound: float = upper_bound
        self.__interval_type: IntervalType = interval_type
        self._func = self.__get_containment_function(self.__interval_type)

    @property
    def interval_id(self) -> str:
        """Returns interval_id of Interval."""
        return self.__interval_id

    @property
    def lower_bound(self) -> float:
        """Returns lower_bound of Interval."""
        return self.__lower_bound

    @property
    def upper_bound(self) -> float:
        """Returns upper_bound of Interval."""
        return self.__upper_bound

    @property
    def interval_type(self) -> IntervalType:
        """Returns interval_type of Interval."""
        return self.__interval_type

    @property
    def func(self):
        """Returns func of Interval."""
        return self._func

    @property
    def is_degenerate(self) -> bool:
        """Control for degenerate"""
        return (self.lower_bound <= self.upper_bound) & (self.lower_bound >= self.upper_bound)

    def __get_containment_function(self, interval_type: IntervalType):

        if interval_type == IntervalType.CLOSED_CLOSED:
            return lambda s: ((s >= self.lower_bound) & (s <= self.upper_bound))
        if interval_type == IntervalType.OPEN_CLOSED:
            return lambda s: ((s > self.lower_bound) & (s <= self.upper_bound))
        if interval_type == IntervalType.CLOSED_OPEN:
            return lambda s: ((s >= self.lower_bound) & (s < self.upper_bound))
        if interval_type == IntervalType.OPEN_OPEN:
            return lambda s: ((s > self.lower_bound) & (s < self.upper_bound))

        raise KnownException("Wrong Interval Type")

    def contains(self, value: float):
        """Check for contains"""
        return self.func(value)

    def deep_copy(self):
        """Deep copy for Interval object"""
        return Interval(self.interval_id, self.lower_bound, self.upper_bound, self.interval_type)

    def to_string(self) -> str:
        """to_string method for Interval object"""
        if self.interval_type == IntervalType.CLOSED_CLOSED:
            return f'[{self.lower_bound},{self.upper_bound}]'
        if self.interval_type == IntervalType.CLOSED_OPEN:
            return f'[{self.lower_bound},{self.upper_bound})'
        if self.interval_type == IntervalType.OPEN_CLOSED:
            return f'({self.lower_bound},{self.upper_bound}]'
        if self.interval_type == IntervalType.OPEN_OPEN:
            return f'({self.lower_bound},{self.upper_bound})'
        return ""

    def __eq__(self, interval: "Interval"):
        """Compare interval"""
        if self.is_degenerate == interval.is_degenerate:
            return self.lower_bound == interval.lower_bound
        return False

    def __hash__(self):
        return hash(self.lower_bound)

    def __lt__(self, interval: "Interval"):
        """Compare Interval"""
        if self.is_degenerate == interval.is_degenerate:
            return self.lower_bound < interval.lower_bound
        if interval.is_degenerate:
            return True
        return False

    def __getstate__(self):
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        del state['_func']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._func = self.__get_containment_function(self.__interval_type)
