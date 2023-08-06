"""
This module includes base class for afe report helpers.
"""
import abc

from organon.afe.domain.reporting.abstract_report_helper import AbstractReportHelper
from organon.afe.domain.reporting.afe_model_output import AfeModelOutput
from organon.afe.domain.reporting.afe_output_report import AfeOutputReport


class BaseReportHelper(AbstractReportHelper[AfeModelOutput, AfeOutputReport], metaclass=abc.ABCMeta):
    """
    This class is base abstract class for afe reporting.
    """

    @classmethod
    def generate_afe_report(cls, model_output: AfeModelOutput) -> AfeOutputReport:
        """Creates output report from model output and runtime statistics"""
        report = AfeOutputReport()
        report.model_identifier = model_output.model_identifier
        output_features = model_output.output_features
        report.output_features = output_features
        report.all_features = model_output.all_features
        report.dimension_names_map = cls._get_dimension_names_map(model_output)
        report.transformations = model_output.transformations
        report.execution_time = model_output.runtime_stats.execution_time
        report.memory_usage = model_output.runtime_stats.memory_usage
        report.cpu_usage = model_output.runtime_stats.cpu_usage
        report.event_times = model_output.runtime_stats.event_times
        report.feature_counts_report = cls._get_feature_counts_report(output_features)
        report.final_column_metrics = model_output.final_column_metrics
        return report
