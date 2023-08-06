"""
This module includes AfeReportHelper class.
"""
from organon.afe.domain.reporting.afe_output_report import AfeOutputReport
from organon.afe.domain.reporting.base_report_helper import BaseReportHelper
from organon.afe.domain.reporting.matplotlib_common_functions import MatplotlibCommonFunctions


class AfeMatplotlibReportHelper(BaseReportHelper):
    """Class for reporting afe output using matplotlib"""

    @classmethod
    def generate_afe_report_dashboard(cls, afe_report: AfeOutputReport):
        """Creates afe report dashboard"""
        MatplotlibCommonFunctions.generate_afe_report_dashboard(cls, afe_report)

    @classmethod
    def generate_afe_feature_dashboard(cls, afe_report: AfeOutputReport):
        """Creates a table including afe output features information"""

        return MatplotlibCommonFunctions.generate_afe_feature_dashboard(cls, afe_report)

    @classmethod
    def generate_feature_extended_dashboard(cls, afe_report: AfeOutputReport):
        MatplotlibCommonFunctions.generate_feature_extended_dashboard(afe_report)

    @classmethod
    def generate_feature_importance_dashboard(cls, afe_report: AfeOutputReport, target_index: int = None,
                                              first_x_feature: int = None):
        MatplotlibCommonFunctions.generate_feature_importance_dashboard(afe_report, target_index=target_index,
                                                                        first_x_feature=first_x_feature)

    @classmethod
    def generate_roc_curve_dashboard(cls, afe_report: AfeOutputReport, target_index: int = None, target_class=None):
        MatplotlibCommonFunctions.generate_roc_curve_dashboard(afe_report, target_index=target_index,
                                                               target_class=target_class)

    @classmethod
    def generate_coarse_class_dashboard(cls, afe_report: AfeOutputReport, feature_name: str):
        """Creates bar plot showing transformation map corresponding to given feature"""
        return MatplotlibCommonFunctions.generate_coarse_class_dashboard(afe_report, feature_name)

    @classmethod
    def generate_memory_usage_dashboard(cls, afe_report: AfeOutputReport):
        """Creates a line-scatter plot of memory usage by date"""
        MatplotlibCommonFunctions.generate_memory_usage_dashboard(afe_report)

    @classmethod
    def generate_cpu_usage_dashboard(cls, afe_report: AfeOutputReport):
        """Creates a line-scatter plot of cpu usage by date"""
        MatplotlibCommonFunctions.generate_cpu_usage_dashboard(afe_report)

    @classmethod
    def generate_resource_usage_dashboard(cls, afe_report: AfeOutputReport):
        """Creates a line-scatter plots of memory and cpu usages by date"""
        MatplotlibCommonFunctions.generate_resource_usage_dashboard(afe_report)
