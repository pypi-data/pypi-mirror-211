"""Includes PlotlyCommonFunctions class."""
from typing import TypeVar, Type

from plotly.graph_objs import Scatter, Table, Bar

from organon.afe.domain.reporting.abstract_report_helper import AbstractReportHelper
from organon.afe.domain.reporting.base_afe_output_report import BaseAfeOutputReport
from organon.afe.domain.reporting.plotly_dashboard_helper import get_line_scatter_plot, get_data_table_plot, \
    get_bar_chart, create_figure, figures_to_html, open_html_in_browser

ReportHelperType = TypeVar("ReportHelperType", bound=AbstractReportHelper)


class PlotlyCommonFunctions:
    """Common functions for plotly report helper classes."""

    @classmethod
    def generate_afe_report_dashboard(cls, report_helper_type: Type[ReportHelperType],
                                      afe_report: BaseAfeOutputReport):
        """Creates afe report dashboard"""
        fig1 = cls._get_afe_feature_dashboard_figure(report_helper_type, afe_report)
        fig2 = cls._get_resource_usage_dashboard_figure(afe_report)
        html = figures_to_html([fig1, fig2])
        open_html_in_browser(html)
        return [fig1, fig2]

    @classmethod
    def generate_afe_feature_dashboard(cls, report_helper_type: Type[ReportHelperType],
                                       afe_report: BaseAfeOutputReport):
        """Creates a table including afe output features information"""
        fig = cls._get_afe_feature_dashboard_figure(report_helper_type, afe_report)
        fig.show()

    @classmethod
    def _get_afe_feature_dashboard_figure(cls, report_helper_type: Type[ReportHelperType],
                                          afe_report: BaseAfeOutputReport):
        """Creates a table including afe output features information"""
        table = cls.__get_afe_feature_table(report_helper_type, afe_report)
        fig = create_figure([table], "Afe Features")
        return fig

    @classmethod
    def generate_coarse_class_dashboard(cls, afe_report: BaseAfeOutputReport, feature_name: str):
        """Creates bar plot showing transformation map corresponding to given feature"""
        bar_chart = cls.__get_coarse_class_bar_chart(afe_report, feature_name)
        fig = create_figure([bar_chart], "Coarse Class Dashboard", "Range", "Value")
        fig.show()

        return fig

    @classmethod
    def generate_memory_usage_dashboard(cls, afe_report: BaseAfeOutputReport):
        """Creates a line-scatter plot of memory usage by date"""
        scatter = cls.__get_memory_usage_scatter(afe_report)
        fig = create_figure([scatter], "Memory Usage", "Date", "Usage(MB)")
        cls.__add_event_lines_to_figure(afe_report, fig)
        fig.show()
        return fig

    @classmethod
    def generate_cpu_usage_dashboard(cls, afe_report: BaseAfeOutputReport):
        """Creates a line-scatter plot of cpu usage by date"""
        scatter = cls.__get_cpu_usage_scatter(afe_report)
        fig = create_figure([scatter], "CPU Usage", "Date", "Usage(percentage)")
        cls.__add_event_lines_to_figure(afe_report, fig, for_cpu=True)
        fig.show()
        return fig

    @classmethod
    def generate_resource_usage_dashboard(cls, afe_report: BaseAfeOutputReport):
        """Creates a line-scatter plots of memory and cpu usages by date"""
        fig = cls._get_resource_usage_dashboard_figure(afe_report)
        fig.show()

    @classmethod
    def _get_resource_usage_dashboard_figure(cls, afe_report: BaseAfeOutputReport):
        """Creates a line-scatter plots of memory and cpu usages by date"""
        ts1 = cls.__get_memory_usage_scatter(afe_report)
        ts2 = cls.__get_cpu_usage_scatter(afe_report)

        fig = create_figure([ts1, ts2], "Resource Usages", "Date", ["Memory Usage(MB)", "CPU Usage(percentage)"])
        cls.__add_event_lines_to_figure(afe_report, fig)

        return fig

    @classmethod
    def __get_coarse_class_bar_chart(cls, afe_report: BaseAfeOutputReport, feature_name: str) -> Bar:
        """Returns a plotly Bar object generated for afe transformation map of given feature"""
        _map = afe_report.transformations[feature_name].tabulate_as_text()
        limits = list(_map.keys())
        map_vals = [float(i) for i in list(_map.values())]

        bar_chart = get_bar_chart(limits, map_vals)
        return bar_chart

    @classmethod
    def __get_afe_feature_table(cls, report_helper_type: Type[ReportHelperType],
                                afe_report: BaseAfeOutputReport) -> Table:
        """Returns a plotly Table object storing afe output features information"""
        data_frame = report_helper_type.get_output_features_as_data_frame(afe_report)
        table = get_data_table_plot(data_frame)
        return table

    @classmethod
    def __get_memory_usage_scatter(cls, afe_report: BaseAfeOutputReport) -> Scatter:
        """Returns a plotly Scatter object generated for memory usage by date"""
        usage = afe_report.memory_usage
        scatter = get_line_scatter_plot(list(usage.keys()), list(usage.values()), "Memory Usage")
        return scatter

    @classmethod
    def __get_cpu_usage_scatter(cls, afe_report: BaseAfeOutputReport) -> Scatter:
        """Returns a plotly Scatter object generated for cpu usage by date"""
        usage = afe_report.cpu_usage

        return get_line_scatter_plot(list(usage.keys()), list(usage.values()), "CPU Usage")

    @classmethod
    def __add_event_lines_to_figure(cls, afe_report, fig, for_cpu=False):
        """Adds vertical lines for events in plot"""
        tick_vals = list(afe_report.event_times.values())
        tick_texts = list(afe_report.event_times.keys())
        values_dict = afe_report.memory_usage
        if for_cpu:
            values_dict = afe_report.cpu_usage
        max_val = max(values_dict.values())
        total_time = max(values_dict.keys()) - min(values_dict.keys())
        for i, val in enumerate(tick_vals):
            if i < len(tick_vals) - 1:
                if (tick_vals[i + 1] - val).total_seconds() < total_time.total_seconds() / 100:
                    # prevents annotation overlapping by eliminating steps with a low execution time
                    continue
            fig.add_vline(x=val, line_dash="dot")
            fig.add_annotation(x=val, text=tick_texts[i], y=max_val, textangle=-90)
