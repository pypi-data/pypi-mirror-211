"""Includes FlSortedDict class."""
from typing import TypeVar, Generic, Dict

from sortedcontainers import SortedDict as _SortedDict

KT = TypeVar('KT')
VT = TypeVar('VT')


class SortedDict(Generic[KT, VT]):
    """A sorted dict implementation using sortedcontainers.SortedDict"""

    def __init__(self, values: Dict[KT, VT] = None):
        values = {} if values is None else values
        self._dict = _SortedDict(values)

    def keys(self):
        """returns keysview instance"""
        return self._dict.keys()

    def values(self):
        """returns valuesview instance"""
        return self._dict.values()

    def items(self):
        """returns dict_items instance"""
        return self._dict.items()

    def popitem(self, index=-1):
        """pop item in dict"""
        return self._dict.popitem(index)

    def __getitem__(self, key: KT) -> VT:
        return self._dict[key]

    def __setitem__(self, key: KT, value: VT):
        self._dict[key] = value

    def __len__(self):
        return len(self._dict)

    def __iter__(self):
        return iter(self._dict)

    def __str__(self):
        return str(self._dict)

    def __repr__(self):
        return repr(self._dict)
