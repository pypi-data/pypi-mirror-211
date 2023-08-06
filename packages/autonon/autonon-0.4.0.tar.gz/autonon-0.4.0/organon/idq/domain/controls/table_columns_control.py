"""todo"""
from typing import List

from organon.fl.core.exceptionhandling.known_exception import KnownException
from organon.idq.core.enums.data_entity_type import DataEntityType
from organon.idq.core.enums.dq_comparison_result_code import DqComparisonResultCode
from organon.idq.domain.businessobjects.data_column.dq_data_column import DqDataColumn
from organon.idq.domain.businessobjects.data_column.dq_df_data_column import DqDfDataColumn
from organon.idq.domain.businessobjects.data_column.dq_file_data_column import DqFileDataColumn
from organon.idq.domain.businessobjects.dq_comparison_result import DqComparisonResult
from organon.idq.domain.businessobjects.dq_data_column_collection import DqDataColumnCollection
from organon.idq.domain.controls.base_dq_control import BaseDqControl
from organon.idq.domain.enums.dq_control_type import DqControlType
from organon.idq.domain.enums.dq_test_group_type import DqTestGroupType


class TableColumnsControl(BaseDqControl):
    """Control class for checking if table columns changed, added or removed"""

    @classmethod
    def get_test_group_type(cls) -> DqTestGroupType:
        return DqTestGroupType.TABLE_SCHEMA_CONTROLS

    @staticmethod
    def get_control_type() -> DqControlType:
        return DqControlType.TABLE_COLUMNS

    def get_description(self) -> str:
        return "Table Columns Control"

    def _execute_control(self) -> List[DqComparisonResult]:
        test_bmh = self.comp_context.test_group_info[self.get_test_group_type()].test_bmh
        if test_bmh < 1:
            raise ValueError("Bmh value cannot be less than 1")
        control_results = self.comp_context.control_results
        if len(control_results) == 0:
            raise ValueError("Benchmark result collection can not be empty")

        if self.comp_context.test_calc_result.data_source_stats is None:
            raise KnownException("T calculation result does not contain data source statistics.")

        max_index = max(len(control_results) - test_bmh, 0)
        filtered_controls = control_results[max_index:]
        calc_names = [calc_param.calculation_name for calc_param in self.comp_context.control_parameters]
        filtered_calc_names = calc_names[max_index:]
        test_col_collection = self.comp_context.test_calc_result.data_source_stats.data_column_collection
        results = []

        for i, control in enumerate(filtered_controls):
            if control.data_source_stats is None:
                raise KnownException(
                    f"Calculation {filtered_calc_names[i]} does not contain data source statistics, "
                    f"re-calculation may be required")
            control_col_collection = control.data_source_stats.data_column_collection
            results.extend(self.__compare_col_metadata(control_col_collection, test_col_collection,
                                                       filtered_calc_names[i]))
        return results

    @classmethod
    def __compare_col_metadata(cls, control_collection: DqDataColumnCollection, test_collection: DqDataColumnCollection,
                               calculation_name: str):
        results = []
        for control_col in control_collection:
            col_name = control_col.column_name
            test_col = test_collection.get_column(col_name)

            if test_col is None:
                comp_result = cls._get_comparison_result(
                    data_entity=DataEntityType.COLUMN,
                    data_entity_name=control_col.column_name,
                    result_code=DqComparisonResultCode.COLUMN_REMOVED,
                    property_code="RemovedColumnName",
                    message=f"Column {control_col.column_name} is removed"
                )
                comp_result.property_key_nominal = control_col.column_name
                comp_result.property_value_nominal = calculation_name
                results.append(comp_result)

            else:
                results.extend(cls._get_column_change_results(control_col, test_col, calculation_name))

        for col in test_collection:
            col_name = col.column_name
            control_col = control_collection.get_column(col_name)
            if control_col is not None:
                continue
            comp_result = cls._get_comparison_result(
                data_entity=DataEntityType.COLUMN,
                data_entity_name=col_name,
                result_code=DqComparisonResultCode.COLUMN_ADDED,
                property_code="AddedColumnName",
                message=f"Column {col_name} is added"
            )
            comp_result.property_key_nominal = col_name
            comp_result.property_value_nominal = calculation_name
            results.append(comp_result)
        return results

    @classmethod
    def _get_column_change_results(cls, control_col: DqDataColumn, test_col: DqDataColumn, calculation_name: str):
        if isinstance(control_col, DqDfDataColumn) and isinstance(test_col, DqDfDataColumn):
            return TableColumnsControl.__get_column_change_results_for_df_column(control_col, test_col,
                                                                                 calculation_name)
        if isinstance(control_col, DqFileDataColumn) and isinstance(test_col, DqFileDataColumn):
            return TableColumnsControl.__get_column_change_results_for_file_column(control_col, test_col,
                                                                                   calculation_name)
        raise NotImplementedError

    @staticmethod
    def __get_column_change_results_for_file_column(control_col: DqFileDataColumn, test_col: DqFileDataColumn,
                                                    calculation_name: str) -> List[DqComparisonResult]:
        message = ""

        if control_col.col_np_dtype != test_col.col_np_dtype:
            message += f"Control Column Data Type: {control_col.col_np_dtype}, " \
                       f"Test Column Data Type: {test_col.col_np_dtype}\n"

        return TableColumnsControl._get_col_type_changed_results(control_col, test_col, message, calculation_name)

    @staticmethod
    def __get_column_change_results_for_df_column(control_col: DqDfDataColumn, test_col: DqDfDataColumn,
                                                  calculation_name: str) -> List[DqComparisonResult]:
        message = ""

        if control_col.col_np_dtype != test_col.col_np_dtype:
            message += f"Control Column Data Type: {control_col.col_np_dtype}, " \
                       f"Test Column Data Type: {test_col.col_np_dtype}\n"

        return TableColumnsControl._get_col_type_changed_results(control_col, test_col, message, calculation_name)

    @classmethod
    def _get_col_type_changed_results(cls, control_col: DqDataColumn, test_col, message: str, calculation_name: str):
        results = []
        if message != "":
            comp_result1 = cls._get_comparison_result(
                data_entity=DataEntityType.COLUMN,
                data_entity_name=control_col.column_name,
                result_code=DqComparisonResultCode.COLUMN_TYPE_CHANGED,
                property_code="PreviousColumn",
                message=message
            )
            comp_result1.property_key_nominal = control_col.column_name
            comp_result1.property_value_nominal = calculation_name
            results.append(comp_result1)
            comp_result2 = cls._get_comparison_result(
                data_entity=DataEntityType.COLUMN,
                data_entity_name=control_col.column_name,
                result_code=DqComparisonResultCode.COLUMN_TYPE_CHANGED,
                property_code="CurrentColumn",
                message=message
            )
            comp_result2.property_key_nominal = test_col.column_name
            comp_result2.property_value_nominal = calculation_name
            results.append(comp_result2)
        return results
