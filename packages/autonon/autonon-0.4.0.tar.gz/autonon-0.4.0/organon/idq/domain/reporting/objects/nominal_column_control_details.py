"""Includes NominalColumnControlDetails class"""

from organon.fl.core.enums.column_native_type import ColumnNativeType


class NominalColumnControlDetails:
    """Class for NominalColumnControlDetails """

    def __init__(self):
        self.calculation_name: str = None
        self.column_name: str = None
        self.column_type: ColumnNativeType = None
        self.percentage: float = None
        self.state_of_benchmark: int = None
        self.value: str = None

    def to_dict(self):
        """return dict for base alert info"""
        return {
            'calculation_name': self.calculation_name,
            'column_name': self.column_name,
            'column_type': self.column_type.name,
            'percentage': self.percentage,
            'state_of_benchmark': self.state_of_benchmark,
            'value': self.value,

        }
