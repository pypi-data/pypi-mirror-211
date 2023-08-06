"""Includes SignalDetails class"""
from organon.idq.core.enums.dq_comparison_result_code import DqComparisonResultCode


class SignalDetails:
    """Class for signal details """

    def __init__(self):
        self.data_entity_name: str = None
        self.column_type: str = None
        self.signal: DqComparisonResultCode = None

    def to_dict(self):
        """return dict for signal detail"""
        return {
            'data_entity_name': self.data_entity_name,
            'column_type': self.column_type,
            'signal': self.signal
        }
