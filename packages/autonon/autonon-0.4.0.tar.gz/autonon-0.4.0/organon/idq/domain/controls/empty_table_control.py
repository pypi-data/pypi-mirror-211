"""todo"""
from typing import List

from organon.fl.core.exceptionhandling.known_exception import KnownException
from organon.idq.core.enums.data_entity_type import DataEntityType
from organon.idq.core.enums.dq_comparison_result_code import DqComparisonResultCode
from organon.idq.domain.businessobjects.dq_comparison_result import DqComparisonResult
from organon.idq.domain.controls.base_dq_control import BaseDqControl
from organon.idq.domain.enums.dq_control_type import DqControlType
from organon.idq.domain.enums.dq_test_group_type import DqTestGroupType


class EmptyTableControl(BaseDqControl):
    """todo"""

    @classmethod
    def get_test_group_type(cls) -> DqTestGroupType:
        return DqTestGroupType.TABLE_SCHEMA_CONTROLS

    @staticmethod
    def get_control_type() -> DqControlType:
        return DqControlType.EMPTY_TABLE

    def get_description(self) -> str:
        return "Empty Table Control"

    def _execute_control(self) -> List[DqComparisonResult]:
        if self.comp_context.test_calc_result is None:
            raise ValueError("T-Calculation result is None.")
        if self.comp_context.test_calc_result.data_source_stats is None:
            raise KnownException("T-Calculation does not contain data source statistics, "
                                 "re-calculation may be required")
        if self.comp_context.test_calc_result.data_source_stats.row_count > 0:
            return []
        input_source = self.comp_context.test_calc_parameters.input_source_settings.source
        result = self._get_comparison_result(
            data_entity=DataEntityType.TABLE,
            data_entity_name=input_source.get_name(),
            result_code=DqComparisonResultCode.TABLE_IS_EMPTY,
            property_code="TableEmpty",
            message=f"Empty data in {input_source.get_name()}"
        )
        result.property_key_nominal = "True"
        return [result]
