"""Includes NumericColumnControlDetails class"""

from organon.fl.core.enums.column_native_type import ColumnNativeType


class NumericColumnControlDetails:
    """Class for NumericColumnControlDetails """

    def __init__(self):
        self.calculation_name: str = None
        self.column_name: str = None
        self.column_type: ColumnNativeType = None
        self.mean: float = None
        self.trimmed_mean: float = None
        self.state_of_benchmark: int = None

    def to_dict(self):
        """return dict for base alert info"""
        return {
            'calculation_name':  self.calculation_name,
            'column_name': self.column_name,
            'column_type': self.column_type.name,
            'mean': self.mean,
            'trimmed_mean': self.trimmed_mean,
            'state_of_benchmark': self.state_of_benchmark
        }
