"""Includes TableControlDetails class"""

from organon.idq.core.enums.data_entity_type import DataEntityType


class TableControlDetails:
    """Class for TableControlDetails """

    def __init__(self):
        self.calculation_name: str = None
        self.type: DataEntityType = None
        self.property_key: str = None
        self.value: int = None
        self.state_of_benchmark: int = None

    def to_dict(self):
        """return dict for base alert info"""
        return {
            'calculation_name': self.calculation_name,
            'type': self.type.name,
            'property_key': self.property_key,
            'value': self.value,
            'state_of_benchmark': self.state_of_benchmark,

        }
