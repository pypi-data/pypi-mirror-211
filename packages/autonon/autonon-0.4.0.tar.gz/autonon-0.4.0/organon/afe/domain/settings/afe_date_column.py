"""
This module includes AfeDateColumn class.
"""
from organon.afe.domain.common.reader_helper import get_values_from_kwargs
from organon.afe.domain.enums.afe_date_column_type import AfeDateColumnType


class AfeDateColumn:
    """
    Class for columns of type date
    """

    ATTR_DICT = {
        "column_name": str,
        "date_column_type": AfeDateColumnType,
        "custom_format": str,
        "db_custom_format": str
    }

    def __init__(self, **kwargs):
        self.column_name: str = None
        self.date_column_type: AfeDateColumnType = None
        self.custom_format: str = None
        self.db_custom_format: str = None

        get_values_from_kwargs(self, AfeDateColumn.ATTR_DICT, kwargs)

    def __deepcopy__(self, memo):
        output = AfeDateColumn()
        output.column_name = self.column_name
        output.date_column_type = self.date_column_type
        output.custom_format = self.custom_format
        output.db_custom_format = self.db_custom_format
        return output
