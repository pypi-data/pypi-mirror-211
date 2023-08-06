"""Class for Psi Signal Control"""
from abc import ABC
from typing import List, Dict

from organon.idq.core.enums.data_entity_type import DataEntityType
from organon.idq.core.enums.dq_comparison_result_code import DqComparisonResultCode
from organon.idq.core.helpers.formatting_helper import FormattingHelper
from organon.idq.domain.businessobjects.dq_calculation_result import DqCalculationResult
from organon.idq.domain.businessobjects.dq_comparison_result import DqComparisonResult
from organon.idq.domain.businessobjects.dq_test_group import DqTestGroup
from organon.idq.domain.controls.base_dq_control import BaseDqControl
from organon.idq.domain.enums.dq_test_group_type import DqTestGroupType
from organon.idq.domain.enums.signal_type import SignalType
from organon.idq.domain.settings.dq_comparison_column_info import DqComparisonColumnInfo


class BasePsiSignalControl(BaseDqControl, ABC):
    """Base class for Psi Signal Control"""

    @classmethod
    def get_test_group_type(cls) -> DqTestGroupType:
        return DqTestGroupType.DISTRIBUTIONAL_COMPARISONS

    def check_maximum_psi(self, col_name: str, result_code: DqComparisonResultCode,
                          results: List[DqComparisonResult], max_psi: float, property_key: str):
        """Result for MaximumPsi"""
        result = DqComparisonResult(
            data_entity=DataEntityType.COLUMN,
            data_entity_name=col_name,
            test_group=self.get_test_group_type(),
            result_code=result_code,
            property_code=property_key,
            message=f"Distribution is unstable for the nominal column {col_name}")
        result.property_key_numeric = FormattingHelper.to_nullable(max_psi)
        results.append(result)

    def check_maximum_psi_control_set(self, col_name: str, result_code: DqComparisonResultCode,
                                      results: List[DqComparisonResult], maximum_psi_sample: str, property_key: str):
        """Result for MaximumPsiControlSet"""
        result = DqComparisonResult(
            data_entity=DataEntityType.COLUMN,
            data_entity_name=col_name,
            test_group=self.get_test_group_type(),
            result_code=result_code,
            property_code=property_key,
            message=f"Distribution is unstable for the nominal column {col_name}")
        result.property_key_nominal = maximum_psi_sample
        results.append(result)

    def check_maximum_psi_category(self, col_name: str, result_code: DqComparisonResultCode,
                                   results: List[DqComparisonResult], maximum_psi_category: str, property_code: str):
        """Result for MaximumPsiCategory"""
        result = DqComparisonResult(
            data_entity=DataEntityType.COLUMN,
            data_entity_name=col_name,
            test_group=self.get_test_group_type(),
            result_code=result_code,
            property_code=property_code,
            message=f"Distribution is unstable for the nominal column {col_name}")
        result.property_key_nominal = maximum_psi_category
        results.append(result)

    def check_test_frequency(self, col_name: str, result_code: DqComparisonResultCode,
                             results: List[DqComparisonResult], test_frequencies: Dict[object, float],
                             property_key: str):
        "Result for TestFrequencies"
        if test_frequencies is not None:
            for test_frequency_key, test_frequency_value in test_frequencies.items():
                result = DqComparisonResult(
                    data_entity=DataEntityType.COLUMN,
                    data_entity_name=col_name,
                    test_group=self.get_test_group_type(),
                    result_code=result_code,
                    property_code=property_key,
                    message=f"Distribution is unstable for the nominal column {col_name}")
                result.property_key_nominal = test_frequency_key
                result.property_key_numeric = FormattingHelper.to_nullable(test_frequency_value)
                results.append(result)

    def check_max_psi_control_frequency(self, col_name: str, result_code: DqComparisonResultCode,
                                        results: List[DqComparisonResult],
                                        maximum_psi_control_set_frequencies: Dict[str, float], property_key: str):
        """Test for MaximumPsiControlFrequencies"""
        if maximum_psi_control_set_frequencies is not None:
            for control_set_frequency_key, control_set_frequency_value \
                    in maximum_psi_control_set_frequencies.items():
                result = DqComparisonResult(
                    data_entity=DataEntityType.COLUMN,
                    data_entity_name=col_name,
                    test_group=self.get_test_group_type(),
                    result_code=result_code,
                    property_code=property_key,
                    message=f"Distribution is unstable for the nominal column {col_name}")
                result.property_key_nominal = control_set_frequency_key
                result.property_key_numeric = FormattingHelper.to_nullable(control_set_frequency_value)
                results.append(result)

    def check_psi_per_control_set(self, col_name: str, result_code: DqComparisonResultCode,
                                  results: List[DqComparisonResult],
                                  psi_per_control_set: Dict[str, float], property_code: str):
        """Test for PsiPerControlSet"""
        if len(psi_per_control_set) > 0:
            for control_set_psi_key, control_set_psi_value in psi_per_control_set.items():
                result = DqComparisonResult(
                    data_entity=DataEntityType.COLUMN,
                    data_entity_name=col_name,
                    test_group=self.get_test_group_type(),
                    result_code=result_code,
                    property_code=property_code,
                    message=f"Distribution is unstable for the nominal column {col_name}")
                result.property_key_nominal = str(control_set_psi_key)
                result.property_key_numeric = FormattingHelper.to_nullable(control_set_psi_value)
                results.append(result)

    def get_signal_type(self, max_psi: float) -> SignalType:
        """Return Signal Type """
        psi_threshold_yellow = self.comp_context.comparison_parameters.psi_threshold_green
        psi_threshold_red = self.comp_context.comparison_parameters.psi_threshold_yellow
        if max_psi < psi_threshold_yellow:
            psi_signal = SignalType.GREEN
        elif max_psi < psi_threshold_red:
            psi_signal = SignalType.YELLOW
        else:
            psi_signal = SignalType.RED
        return psi_signal

    def _get_filtered_columns(self, col: DqComparisonColumnInfo, test_group_info: DqTestGroup) -> \
            List[DqCalculationResult]:
        effective_bmh = min(test_group_info.test_bmh, col.benchmark_horizon)
        max_index = max(len(self.comp_context.control_results) - effective_bmh, 0)
        filtered_controls = list(reversed(self.comp_context.control_results[max_index:]))
        return filtered_controls
