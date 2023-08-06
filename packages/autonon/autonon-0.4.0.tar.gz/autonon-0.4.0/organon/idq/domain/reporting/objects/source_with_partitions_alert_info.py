"""Includes SourceWithPartitionsAlertInfo class"""
from organon.fl.core.helpers import string_helper
from organon.idq.domain.reporting.objects.base_alert_info import BaseAlertInfo


class SourceWithPartitionsAlertInfo(BaseAlertInfo):
    """Alert Info for One DF with Date Info"""

    def to_dict(self):
        """return dict for base alert info"""
        if string_helper.is_null_or_empty(self.full_filter_str):
            return {
                'data_source_name': self.data_source_name,
                'alert': self.alert,
                'run_type': self.run_type.name,
            }
        return {
            'data_source_name': self.data_source_name,
            'filter': self.full_filter_str,
            'alert': self.alert,
            'run_type': self.run_type.name,
        }
