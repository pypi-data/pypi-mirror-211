"""
This module includes AfeTargetColumn class.
"""
from organon.afe.domain.common.reader_helper import get_values_from_kwargs
from organon.afe.domain.enums.afe_target_column_type import AfeTargetColumnType
from organon.afe.domain.settings.binary_target import BinaryTarget


class AfeTargetColumn:
    """
    Information for target column of Automated Feature Extraction process
    """
    ATTR_DICT = {
        "column_name": str,
        "target_column_type": AfeTargetColumnType,
        "binary_target_info": BinaryTarget
    }

    def __init__(self, **kwargs):
        self.column_name: str = None
        self.target_column_type: AfeTargetColumnType = None
        self.binary_target_info: BinaryTarget = None

        get_values_from_kwargs(self, self.ATTR_DICT, kwargs)
