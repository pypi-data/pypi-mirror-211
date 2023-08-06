"""
This module includes AfePlotlyReportHelper class.
"""
from organon.afe.domain.reporting.base_afe_output_report import BaseAfeOutputReport
from organon.afe.domain.reporting.base_report_helper import BaseReportHelper
from organon.afe.domain.reporting.plotly_common_functions import PlotlyCommonFunctions


class AfePlotlyReportHelper(BaseReportHelper):
    """Class for reporting afe output using plotly"""

    @classmethod
    def generate_feature_extended_dashboard(cls, afe_report: BaseAfeOutputReport):
        raise NotImplementedError

    @classmethod
    def generate_feature_importance_dashboard(cls, afe_report: BaseAfeOutputReport, target_index: int = None,
                                              first_x_feature: int = None):
        raise NotImplementedError

    @classmethod
    def generate_roc_curve_dashboard(cls, afe_report: BaseAfeOutputReport, target_index: int = None, target_class=None):
        raise NotImplementedError

    @classmethod
    def generate_afe_report_dashboard(cls, afe_report: BaseAfeOutputReport):
        """Creates afe report dashboard"""
        PlotlyCommonFunctions.generate_afe_report_dashboard(cls, afe_report)

    @classmethod
    def generate_afe_feature_dashboard(cls, afe_report: BaseAfeOutputReport):
        """Creates a table including afe output features information"""
        PlotlyCommonFunctions.generate_afe_feature_dashboard(cls, afe_report)

    @classmethod
    def generate_coarse_class_dashboard(cls, afe_report: BaseAfeOutputReport, feature_name: str):
        """Creates bar plot showing transformation map corresponding to given feature"""
        return PlotlyCommonFunctions.generate_coarse_class_dashboard(afe_report, feature_name)

    @classmethod
    def generate_memory_usage_dashboard(cls, afe_report: BaseAfeOutputReport):
        """Creates a line-scatter plot of memory usage by date"""
        return PlotlyCommonFunctions.generate_memory_usage_dashboard(afe_report)

    @classmethod
    def generate_cpu_usage_dashboard(cls, afe_report: BaseAfeOutputReport):
        """Creates a line-scatter plot of cpu usage by date"""
        return PlotlyCommonFunctions.generate_cpu_usage_dashboard(afe_report)

    @classmethod
    def generate_resource_usage_dashboard(cls, afe_report: BaseAfeOutputReport):
        """Creates a line-scatter plots of memory and cpu usages by date"""
        PlotlyCommonFunctions.generate_resource_usage_dashboard(afe_report)
