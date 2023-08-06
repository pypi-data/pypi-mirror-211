"""Includes TupleGenericCollection class."""
from typing import TypeVar, List, Generic, Tuple, Dict

from sortedcontainers import SortedDict

T = TypeVar("T")  # pylint: disable=invalid-name


class TupleGenericCollection(Generic[T]):
    """A collection storing value-tuple mappings. There is a maximum number(capacity) of tuples that can be stored."""

    def __init__(self, capacity: int):
        self.__capacity: int = capacity
        self.__list_per_tuple: Dict[Tuple, List[T]] = SortedDict()
        self.__tuple_reverse_list: Dict[T, Tuple] = SortedDict()

    def try_add(self, _tuple: Tuple, datum: T) -> bool:
        """Adds given _tuple-datum mapping to collection if capacity is not exceeded."""
        if _tuple not in self.__list_per_tuple:
            if len(self.__list_per_tuple) >= self.__capacity:
                return False
            self.__list_per_tuple[_tuple] = []
        self.__list_per_tuple[_tuple].append(datum)
        self.__tuple_reverse_list[datum] = _tuple
        return True

    @property
    def count(self):
        """Returns number of tuple mappings in collection."""
        return len(self.__list_per_tuple)

    @property
    def capacity(self):
        """Returns capacity of collection."""
        return self.__capacity

    def __getitem__(self, datum: T):
        return self.__tuple_reverse_list[datum]

    @property
    def list_per_tuple(self):
        """Returns tuple-value_list mapping in collection."""
        return self.__list_per_tuple
