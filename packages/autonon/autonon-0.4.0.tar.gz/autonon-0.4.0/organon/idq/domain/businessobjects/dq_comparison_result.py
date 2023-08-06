"""Includes DqComparisonResult class"""
from typing import Optional, Union

from organon.idq.core.enums.data_entity_type import DataEntityType
from organon.idq.core.enums.dq_comparison_result_code import DqComparisonResultCode
from organon.idq.core.helpers.formatting_helper import FormattingHelper
from organon.idq.domain.enums.dq_test_group_type import DqTestGroupType


class DqComparisonResult:
    """todo"""

    def __init__(self, data_entity: DataEntityType, data_entity_name: str,
                 test_group: DqTestGroupType, result_code: DqComparisonResultCode = None,
                 message: str = None, property_code: str = None
                 ):
        self.data_entity = data_entity
        self.data_entity_name = data_entity_name
        self.test_group = test_group
        self.result_code = result_code
        self.message = message
        self.property_code = property_code
        self.property_key_numeric: Optional[float] = None
        self.property_key_nominal: Optional[str] = None
        self.property_value_numeric: Optional[float] = None
        self.property_value_nominal: Optional[str] = None
        self.signal_type = None

    def set_property_key(self, key: Union[str, float]):
        """Sets property_key_nominal/property_key_numeric value"""
        if isinstance(key, str):
            self.property_key_nominal = key
        elif isinstance(key, float):
            self.property_key_numeric = FormattingHelper.to_nullable(key)
        else:
            raise ValueError("key should be either str or float")

    def set_property_key_value_pair(self, key: Union[str, float], value: Union[str, float]):
        """Sets property_key-propertyvalue pair"""
        self.set_property_key(key)
        if isinstance(value, str):
            self.property_value_nominal = value
        elif isinstance(value, float):
            self.property_value_numeric = FormattingHelper.to_nullable(value)
        else:
            raise ValueError("Value should be either str or float")
