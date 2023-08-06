"""
This module includes TransactionFileRecord class.
"""
import numpy as np


class TransactionFileRecord:
    """
    Class corresponding to a row in a transaction file
    """

    def __init__(self, date: float, q_array: np.ndarray, d_array: np.ndarray):
        self.__date: float = date
        self.__q_array: np.ndarray = q_array
        self.__d_array: np.ndarray = d_array

    @property
    def date(self) -> float:
        """Returns value of private attribute '__date'"""
        return self.__date

    def get_quantity(self, index: int) -> np.float64:
        """Returns value of element in given index of private list '__q_array'"""
        return self.__q_array[index]

    def get_dimension(self, index: int) -> np.short:
        """Returns value of element in given index of private list '__d_array'"""
        return self.__d_array[index]

    def __lt__(self, other) -> bool:
        """Allows 'less than' comparison between TransactionFileRecord instances based on __date attribute"""
        return not self.date < other.date
