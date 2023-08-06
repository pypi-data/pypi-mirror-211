"""todo"""

import abc
from typing import List

from organon.fl.logging.helpers.log_helper import LogHelper
from organon.idq.core.enums.data_entity_type import DataEntityType
from organon.idq.core.enums.dq_comparison_result_code import DqComparisonResultCode

from organon.idq.domain.businessobjects.dq_comparison_result import DqComparisonResult
from organon.idq.domain.businessobjects.dq_control_parameters import DqControlParameters
from organon.idq.domain.enums.dq_control_type import DqControlType
from organon.idq.domain.enums.dq_test_group_type import DqTestGroupType


class BaseDqControl(metaclass=abc.ABCMeta):
    """todo"""

    def __init__(self, dq_comparison_context: DqControlParameters):
        self.comp_context = dq_comparison_context

    def execute(self) -> List[DqComparisonResult]:
        """todo"""
        control_description = self.get_description()

        LogHelper.info(f"Executing control: {control_description}")
        results = self._execute_control()

        LogHelper.info(f"Finished executing control: {control_description}")
        return results

    @classmethod
    def _get_comparison_result(cls, data_entity: DataEntityType, data_entity_name: str,
                               result_code: DqComparisonResultCode = None,
                               message: str = None, property_code: str = None):
        return DqComparisonResult(
            data_entity=data_entity, data_entity_name=data_entity_name, test_group=cls.get_test_group_type(),
            result_code=result_code, message=message, property_code=property_code
        )

    @classmethod
    @abc.abstractmethod
    def get_test_group_type(cls) -> DqTestGroupType:
        """return group type of dq control"""

    @staticmethod
    @abc.abstractmethod
    def get_control_type() -> DqControlType:
        """return control type"""

    @abc.abstractmethod
    def _execute_control(self) -> List[DqComparisonResult]:
        pass

    @abc.abstractmethod
    def get_description(self) -> str:
        """todo"""

    def get_test_bmh(self):
        """Returns max benchmark horizon for comparison"""
        return self.comp_context.test_group_info[self.get_test_group_type()].test_bmh
