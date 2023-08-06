"""
This module includes base class for afe report helpers.
"""
import abc
from typing import Dict, TypeVar, Generic, List

import pandas as pd


from organon.afe.domain.common.persist_helper import PersistHelper
from organon.afe.domain.modelling.businessobjects.base_afe_feature import BaseAfeFeature
from organon.afe.domain.reporting.base_afe_model_output import BaseAfeModelOutput
from organon.afe.domain.reporting.base_afe_output_report import FeatureCountReport, BaseAfeOutputReport

AfeModelOutputType = TypeVar("AfeModelOutputType", bound=BaseAfeModelOutput)
AfeOutputReportType = TypeVar("AfeOutputReportType", bound=BaseAfeOutputReport)


class AbstractReportHelper(Generic[AfeModelOutputType, AfeOutputReportType], metaclass=abc.ABCMeta):
    """
    This class is base abstract class for afe reporting.
    """

    @classmethod
    def __get_count_by_quantity_col(cls, output_features: Dict[str, BaseAfeFeature]):
        count_dict = {}
        for feature in output_features.values():
            qty_name = feature.afe_column.quantity_name
            if qty_name in count_dict:
                count_dict[qty_name] += 1
            else:
                count_dict[qty_name] = 1
        return count_dict

    @classmethod
    def __get_count_by_dimension_col(cls, output_features: Dict[str, BaseAfeFeature]):
        count_dict = {}
        for feature in output_features.values():
            dimension = feature.afe_column.dimension_name
            if dimension in count_dict:
                count_dict[dimension] += 1
            else:
                count_dict[dimension] = 1
        return count_dict

    @classmethod
    def __get_count_by_operator(cls, output_features: Dict[str, BaseAfeFeature]):
        count_dict = {}
        for feature in output_features.values():
            op_name = feature.afe_column.operator.name
            if op_name in count_dict:
                count_dict[op_name] += 1
            else:
                count_dict[op_name] = 1
        return count_dict

    @classmethod
    def _get_count_by_time_window(cls, output_features: Dict[str, BaseAfeFeature]):
        count_dict = {}
        for feature in output_features.values():
            time_window = feature.afe_column.time_window
            val = str(time_window)
            if val in count_dict:
                count_dict[val] += 1
            else:
                count_dict[val] = 1
        return count_dict

    @classmethod
    def _get_feature_counts_report(cls, output_features: Dict[str, BaseAfeFeature]):
        by_dim = AbstractReportHelper.__get_count_by_dimension_col(output_features)
        by_qty = AbstractReportHelper.__get_count_by_quantity_col(output_features)
        by_op = AbstractReportHelper.__get_count_by_operator(output_features)
        by_tw = AbstractReportHelper._get_count_by_time_window(output_features)
        return FeatureCountReport(by_dim, by_qty, by_op, by_tw)

    @classmethod
    def _get_dimension_names_map(cls, model_output: AfeModelOutputType):
        features = model_output.all_features if model_output.all_features is not None else model_output.output_features
        all_dimensions = [feature.afe_column.dimension_name for feature in features.values()]
        names_map = {}
        for dim in all_dimensions:
            names_map[dim] = model_output.transaction_file_stats.get_histogram(dim).reverse_index
        return names_map

    @classmethod
    @abc.abstractmethod
    def generate_afe_report(cls, model_output: AfeModelOutputType) -> AfeOutputReportType:
        """Creates output report from model output and runtime statistics"""

    @classmethod
    @abc.abstractmethod
    def generate_afe_report_dashboard(cls, afe_report: AfeOutputReportType):
        """Creates afe report dashboard"""
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def generate_afe_feature_dashboard(cls, afe_report: AfeOutputReportType):
        """Creates a table including afe output features information"""
        raise NotImplementedError

    @classmethod
    def generate_feature_extended_dashboard(cls, afe_report: AfeOutputReportType):
        """Creates extended feature report"""
        raise NotImplementedError

    @classmethod
    def generate_feature_importance_dashboard(cls, afe_report: AfeOutputReportType, target_index: int = None,
                                              first_x_feature: int = None):
        """Creates afe feature importance dashboard"""
        raise NotImplementedError

    @classmethod
    def generate_roc_curve_dashboard(cls, afe_report: AfeOutputReportType, target_index: int = None, target_class=None):
        """Creates roc curve plot for features in given target"""
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def generate_coarse_class_dashboard(cls, afe_report: AfeOutputReportType, feature_name: str):
        """Creates bar plot showing transformation map corresponding to given feature"""
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def generate_memory_usage_dashboard(cls, afe_report: AfeOutputReportType):
        """Creates a line-scatter plot of memory usage by date"""
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def generate_cpu_usage_dashboard(cls, afe_report: AfeOutputReportType):
        """Creates a line-scatter plot of cpu usage by date"""
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def generate_resource_usage_dashboard(cls, afe_report: AfeOutputReportType):
        """Creates a line-scatter plots of memory and cpu usages by date"""
        raise NotImplementedError

    @classmethod
    def get_output_features_as_data_frame(cls, afe_report: AfeOutputReportType):
        """Creates and returns a data frame of output features information"""
        features = list(afe_report.output_features.values())
        return cls._get_features_as_df(afe_report.dimension_names_map, features)

    @classmethod
    def _get_features_as_df(cls, dimension_names_map: Dict[str, Dict[int, str]], features: List[BaseAfeFeature]):
        col_info = []
        for feature in features:
            afe_col = feature.afe_column
            dimension = feature.afe_column.dimension_name
            dimension_names_dict = dimension_names_map[dimension] if dimension in dimension_names_map else {}
            meaning = cls.get_feature_meaning(feature, dimension_names_dict)
            tw_str = cls._get_time_window_string(feature)
            col_info.append(
                {
                    "Feature": feature.feature_name,
                    "Dimension": afe_col.dimension_name,
                    "Quantity": afe_col.quantity_name,
                    "Operator": afe_col.operator.name,
                    "Date Column": afe_col.date_column.column_name if afe_col.date_column is not None else "",
                    "Time Window": tw_str,
                    "Resolution": afe_col.date_resolution.name,
                    "Meaning": meaning
                }
            )

        data_frame = pd.DataFrame(col_info)
        data_frame.fillna('', inplace=True)

        return data_frame

    @classmethod
    def _get_time_window_string(cls, afe_feature:BaseAfeFeature):
        return str(afe_feature.afe_column.time_window)

    @classmethod
    def get_feature_meaning(cls, feature: BaseAfeFeature, group_names: Dict[int, str]) -> str:
        """Returns meaning of given afe output feature"""
        return PersistHelper.get_feature_meaning(feature, group_names)
