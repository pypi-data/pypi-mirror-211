"""Includes FlSortedList class."""
from typing import List, TypeVar, Generic

from sortedcontainers import SortedList as _SortedList

T = TypeVar('T')


class SortedList(Generic[T]):
    """A sorted list implementation using sortedcontainers.SortedList"""

    def __init__(self, values: List[T] = None):
        values = [] if values is None else values
        self._list = _SortedList(values)

    def add(self, value: T):
        """Add element to list"""
        self._list.add(value)

    def __getitem__(self, index):
        return self._list[index]

    def __len__(self):
        return len(self._list)

    def __iter__(self):
        return iter(self._list)

    def __str__(self):
        return str(self._list)

    def __repr__(self):
        return repr(self._list)
