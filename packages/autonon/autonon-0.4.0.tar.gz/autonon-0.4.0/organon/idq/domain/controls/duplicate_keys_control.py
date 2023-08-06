"""Includes DuplicateKeysControl class"""
from typing import List

import pandas as pd

from organon.idq.core.enums.data_entity_type import DataEntityType
from organon.idq.core.enums.dq_comparison_result_code import DqComparisonResultCode
from organon.idq.domain.businessobjects.dq_comparison_result import DqComparisonResult
from organon.idq.domain.controls.base_dq_control import BaseDqControl
from organon.idq.domain.enums.dq_control_type import DqControlType
from organon.idq.domain.enums.dq_test_group_type import DqTestGroupType
from organon.idq.domain.settings.input_source.dq_df_input_source_settings import DqDfInputSourceSettings
from organon.idq.domain.settings.input_source.dq_file_input_source_settings import DqFileInputSourceSettings


class DuplicateKeysControl(BaseDqControl):
    """Control class for checking if duplicate values exist in primary key columns"""

    @classmethod
    def get_test_group_type(cls) -> DqTestGroupType:
        return DqTestGroupType.RULE_BASED_CONTROLS_COLUMN_SET

    @staticmethod
    def get_control_type() -> DqControlType:
        return DqControlType.DUPLICATE_KEYS

    def get_description(self) -> str:
        return "Duplicate Keys Control"

    def _execute_control(self) -> List[DqComparisonResult]:
        key_columns = [col.column_name for col in self.comp_context.comparison_parameters.comparison_columns
                       if col.duplicate_column_control]
        if len(key_columns) == 0:
            return []

        unique_keys_count = self._get_unique_keys_count(key_columns)
        row_count = self.comp_context.test_calc_result.data_source_stats.row_count
        duplicate_rows = row_count - unique_keys_count
        if duplicate_rows <= 0:
            return []
        source_name = self.comp_context.test_calc_parameters.input_source_settings.source.get_name()
        result = self._get_comparison_result(
            data_entity=DataEntityType.TABLE,
            data_entity_name=source_name,
            property_code="DuplicateKeys",
            result_code=DqComparisonResultCode.TABLE_CONTAINS_DUPLICATE_KEYS,
            message=f"{source_name} contains duplicate keys. Row count: {row_count}. Cardinality: {unique_keys_count}. "
                    f"Number of rows with duplicate keys: {duplicate_rows}"
        )
        result.property_key_numeric = duplicate_rows
        return [result]

    def _get_unique_keys_count(self, key_columns: List[str]):
        input_source_settings = self.comp_context.test_calc_parameters.input_source_settings
        source = input_source_settings.source

        if isinstance(input_source_settings, DqDfInputSourceSettings):
            return len(source.locator.groupby(key_columns).groups)
        if isinstance(input_source_settings, DqFileInputSourceSettings):
            unique_keys = set()
            for dataframe in pd.read_csv(source.locator, sep=input_source_settings.csv_separator,
                                         chunksize=input_source_settings.number_of_rows_per_step):
                unique_keys.update(dataframe.groupby(key_columns).groups.keys())
            return len(unique_keys)
        raise ValueError("InputSourceSettings is not of expected types")
