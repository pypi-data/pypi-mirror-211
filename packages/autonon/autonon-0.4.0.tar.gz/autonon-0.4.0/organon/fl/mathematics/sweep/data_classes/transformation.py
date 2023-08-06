"""Module for Transformation"""
from dataclasses import dataclass


@dataclass
class Transformation:
    """Class Description"""
    _default_output_value: int
    _variable_importance: int
    variable_importance_raw: int
    is_stable: bool

    @staticmethod
    def evaluate(inp):
        """Function Description"""
        return inp
