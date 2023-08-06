"""Includes BaseAlertInfo class"""
import abc

from organon.fl.core.helpers import string_helper
from organon.idq.domain.enums.dq_run_type import DqRunType


class BaseAlertInfo(metaclass=abc.ABCMeta):
    """Class for base alert info"""
    def __init__(self):
        self.data_source_name: str = None
        self.full_filter_str: str = None
        self.alert: str = None
        self.run_type: DqRunType = None

    def to_dict(self):
        """return dict for base alert info"""
        if string_helper.is_null_or_empty(self.full_filter_str):
            return {
                'data_source_name': self.data_source_name,
                'alert': self.alert,
                'run_type': self.run_type.name
            }
        return {
            'data_source_name': self.data_source_name,
            'filter': self.full_filter_str,
            'alert': self.alert,
            'run_type': self.run_type.name
        }
