"""
This module includes Pair class.
"""
from typing import TypeVar, Generic, NamedTuple
S1 = TypeVar("S1")
T1 = TypeVar("T1")


class Pair(Generic[S1, T1], NamedTuple("Pair", [('first', S1), ('second', T1)])):
    """
    Class for defining the comparable and generic pair type.
    """
    def __eq__(self, other: "Pair"):
        return self.first == other.first and self.second == other.second

    def __lt__(self, other: "Pair"):
        return self.first < other.first

    def __le__(self, other: "Pair"):
        return self.first <= other.first

    def __gt__(self, other: "Pair"):
        return self.first > other.first

    def __ge__(self, other: "Pair"):
        return self.first >= other.first

    def __str__(self):
        return f"({self.first}, {self.second})"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((self.first, self.second))
