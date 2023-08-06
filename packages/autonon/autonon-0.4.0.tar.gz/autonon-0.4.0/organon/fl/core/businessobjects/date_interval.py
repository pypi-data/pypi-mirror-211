"""
This module keeps DateInterval class.
"""
from datetime import datetime
from typing import Callable, Union

from organon.fl.core.enums.date_interval_type import DateIntervalType


class DateInterval:
    """
    This class is used for checking the date interval types.
    """

    def __init_subclass__(cls, **kwargs):
        raise TypeError("type 'DateInterval' is not an acceptable base type")

    def __init__(self, lower_bound: Union[datetime, int], upper_bound: Union[datetime, int],
                 interval_type: DateIntervalType):
        self.__interval_type: DateIntervalType = interval_type
        self.__lower_bound: Union[datetime, int] = lower_bound
        self.__upper_bound: Union[datetime, int] = upper_bound
        self.__func: Callable[[Union[datetime, int]], bool] = self.get_func(self.__interval_type)

    @property
    def interval_type(self) -> DateIntervalType:
        """
        Returns the date interval type.
        :return: Date interval type of the current object
        """
        return self.__interval_type

    @property
    def lower_bound(self) -> Union[datetime, int]:
        """
        Returns the lower bound datetime.
        :return: lower bound datetime object
        """
        return self.__lower_bound

    @property
    def upper_bound(self) -> Union[datetime, int]:
        """
        Returns the upper bound datetime.
        :return: upper bound datetime object
        """
        return self.__upper_bound

    @property
    def func(self) -> Callable[[Union[datetime, int]], bool]:
        """
        Returns a bool function which takes a datetime object or timesstamp value as a parameter.
        :return: bool function which takes a datetime object or timestamp value as a parameter
        """
        return self.__func

    def get_func(self, interval_type: DateIntervalType) -> Callable[[Union[datetime, int]], bool]:
        """
        Returns a function according to the date interval type.
        :param interval_type: date interval type
        :return: bool function which takes a datetime object as a parameter
        """

        if interval_type == DateIntervalType.CLOSED_CLOSED:
            return self.__closed_closed
        if interval_type == DateIntervalType.OPEN_CLOSED:
            return self.__open_closed
        if interval_type == DateIntervalType.CLOSED_OPEN:
            return self.__closed_open
        if interval_type == DateIntervalType.OPEN_OPEN:
            return self.__open_open
        return self.__default

    def __closed_closed(self, date: Union[datetime, int]) -> bool:
        """
        Checks if the datetime object has closed closed relation between the intervals.
        :param date: datetime object or timestamp value
        :return: bool object which checks whether the datetime object has closed closed relation between the
        intervals
        """
        return self.__lower_bound <= date <= self.__upper_bound

    def __open_closed(self, date: Union[datetime, int]) -> bool:
        """
        Checks if the datetime object has open closed relation between the intervals.
        :param date: datetime object or timestamp
        :return: bool object which checks whether the datetime object has open closed relation between the intervals
        """
        return self.__lower_bound < date <= self.__upper_bound

    def __closed_open(self, date: Union[datetime, int]) -> bool:
        """
        Checks if the datetime object has closed open relation between the intervals.
        :param date: datetime object
        :return: bool object which checks whether the datetime object has closed open relation between the intervals
        """
        return self.__lower_bound <= date < self.__upper_bound

    def __open_open(self, date: Union[datetime, int]) -> bool:
        """
        Checks if the datetime object has open open relation between the intervals.
        :param date: datetime object
        :return: bool object which checks whether the datetime object has open open relation between the intervals
        """
        return self.__lower_bound < date < self.__upper_bound

    def __default(self, date: Union[datetime, int]) -> bool:
        """
        Checks if the datetime object has default relation between the intervals.
        :param date: datetime object
        :return: bool object which checks whether the datetime object has default relation between the intervals
        """
        return self.__lower_bound <= date <= self.__upper_bound

    def contains(self, val: Union[datetime, int]) -> bool:
        """
        Checks if the function contains datetime object.
        :param val: datetime object
        :return: bool object which checks whether the function contains datetime object.
        """
        return self.__func(val)
