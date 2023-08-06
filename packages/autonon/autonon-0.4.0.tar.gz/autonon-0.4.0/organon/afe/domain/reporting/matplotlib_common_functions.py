"""Includes MatplotlibCommonFunctions class."""

from datetime import timedelta
from typing import TypeVar, Type

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes, BarContainer
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator

from organon.afe.domain.reporting import dashboard_helper
from organon.afe.domain.reporting.abstract_report_helper import AbstractReportHelper
from organon.afe.domain.reporting.base_afe_output_report import BaseAfeOutputReport
from organon.afe.domain.reporting.dashboard_helper import TablePagination
# ax kısaltması bir convention
# pylint: disable=invalid-name
from organon.fl.core.exceptionhandling.known_exception import KnownException

ReportHelperType = TypeVar("ReportHelperType", bound=AbstractReportHelper)


class MatplotlibCommonFunctions:
    """Common functions for matplotlib report helper classes."""

    @classmethod
    def generate_afe_report_dashboard(cls, report_helper_type: Type[ReportHelperType], afe_report: BaseAfeOutputReport):
        """Creates afe report dashboard"""
        fig, ax1 = plt.subplots()
        fig.canvas.manager.set_window_title("Output Features")
        ax1.set_title("Output Features")
        ax1.set_axis_off()
        table = cls.__get_afe_feature_table(report_helper_type, afe_report, ax1, rows_per_page=3)
        table.add_buttons(fig)
        plt.show()
        fig, ax2 = plt.subplots()
        fig.canvas.manager.set_window_title("Resource Usage")
        cls.__get_resource_usage_ax(afe_report, ax2)
        plt.show()

    @classmethod
    def generate_afe_feature_dashboard(cls, report_helper_type: Type[ReportHelperType],
                                       afe_report: BaseAfeOutputReport):
        """Creates a table including afe output features information"""

        fig, ax = plt.subplots()
        ax.set_axis_off()
        fig.patch.set_visible(False)
        fig.canvas.manager.set_window_title("Afe Feature Dashboard")
        ax.set_title("Output Features")

        table = cls.__get_afe_feature_table(report_helper_type, afe_report, ax, rows_per_page=10)
        table.add_buttons(fig)

        plt.show()

        return ax

    @classmethod
    def generate_feature_extended_dashboard(cls, afe_report: BaseAfeOutputReport):
        """Creates extended feature report"""

        quantity_summary = cls.__convert_to_df(
            afe_report.feature_counts_report.by_quantity, "Quantity")
        dimension_summary = cls.__convert_to_df(afe_report.feature_counts_report.by_dimension,
                                                "Dimension")
        operator_summary = cls.__convert_to_df(afe_report.feature_counts_report.by_operator,
                                               "Operator")
        tw_summary = cls.__convert_to_df(afe_report.feature_counts_report.by_time_window,
                                         "Time Window")
        total_feature = len(afe_report.output_features)
        rc2 = {"font.size": 8}
        with plt.rc_context(rc2):
            fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(30, 20), constrained_layout=True)
            for ax in axs.reshape(-1):
                ax.xaxis.set_major_locator(MaxNLocator(integer=True))

            sns.barplot(x="Count", y="Quantity", data=quantity_summary, orient="h", ax=axs[0, 0]).set(
                title='Quantity Columns Distribution', ylabel=None)
            cls.__arrange_y_tick_labels(axs[0, 0], quantity_summary["Quantity"])
            sns.barplot(x="Count", y="Dimension", data=dimension_summary, orient="h", ax=axs[0, 1]).set(
                title='Dimension Columns Distribution', ylabel=None)
            cls.__arrange_y_tick_labels(axs[0, 1], dimension_summary["Dimension"])
            sns.barplot(x="Count", y="Operator", data=operator_summary, orient="h", ax=axs[1, 0]).set(
                title='Operators Distribution', ylabel=None)
            cls.__arrange_y_tick_labels(axs[1, 0], operator_summary["Operator"])
            sns.barplot(x="Count", y="Time Window", data=tw_summary, orient="h", ax=axs[1, 1],
                        order=tw_summary['Time Window']).set(title='Time Window Distribution', ylabel=None)
            cls.__arrange_y_tick_labels(axs[1, 1], tw_summary["Time Window"])
            fig.suptitle(f'Total Number of Features: {total_feature}', fontsize=20)
            plt.show()

    @classmethod
    def __arrange_y_tick_labels(cls, ax, tick_labels):
        y_tick_lbl_size = 8 if len(tick_labels) <= 7 else 64 / len(tick_labels)
        max_label_len = max([len(str(label)) for label in tick_labels])
        ax.tick_params(labelsize=y_tick_lbl_size)
        dashboard_helper.wrap_labels(ax, int(2000 / (y_tick_lbl_size * max_label_len)), True, axis="y")

    @classmethod
    def generate_feature_importance_dashboard(cls, afe_report: BaseAfeOutputReport, target_index: int = None,
                                              first_x_feature: int = None):
        """Creates afe feature importance dashboard"""
        if afe_report.final_column_metrics is None:
            raise ValueError("afe report does not include final column metrics")
        metrics_to_report = list(enumerate(afe_report.final_column_metrics))
        if target_index is not None:
            if len(afe_report.final_column_metrics) <= target_index:
                raise KnownException(f"Target with index {target_index} does not exist. "
                                     f"Num targets: {len(afe_report.final_column_metrics)}")
            metrics_to_report = [(target_index, afe_report.final_column_metrics[target_index])]
        for i, metrics in metrics_to_report:
            first_x_feature = first_x_feature if first_x_feature is not None else len(metrics["feature_importances"])
            plt.figure(figsize=(30, 20))
            data = metrics["feature_importances"].sort_values(by="Value", ascending=False)[:first_x_feature]
            sns.barplot(x="Value", y="Feature", data=data, orient="h", order=data["Feature"])
            ax = plt.gca()
            y_tick_lbl_size = 8 if len(data) <= 10 else 90 / len(data)
            ax.tick_params(labelsize=y_tick_lbl_size)
            dashboard_helper.wrap_labels(ax, int(160 / y_tick_lbl_size), True, axis="y")
            plt.title(f"Feature Importances (Target {i + 1})")
            plt.show()

    @classmethod
    def generate_roc_curve_dashboard(cls, afe_report: BaseAfeOutputReport, target_index: int = None, target_class=None):
        """Creates roc curve plot for features in given target"""

        if afe_report.final_column_metrics is None:
            raise ValueError("afe report does not include final column metrics")
        metrics_to_report = list(enumerate(afe_report.final_column_metrics))
        if target_index is not None:
            if len(afe_report.final_column_metrics) <= target_index:
                raise KnownException(f"Target with index {target_index} does not exist. "
                                     f"Num targets: {len(afe_report.final_column_metrics)}")
            metrics_to_report = [(target_index, afe_report.final_column_metrics[target_index])]

        for i, metrics in metrics_to_report:
            if "fpr" not in metrics or "tpr" not in metrics or "auc" not in metrics:
                raise ValueError(f"metrics for target {i} does not include all of required values: (fpr,tpr,auc)")
            fpr_dict, tpr_dict = metrics["fpr"].copy(), metrics["tpr"].copy()
            auc_val_dict = metrics["auc"].copy()
            if len(fpr_dict) > 0 and len(tpr_dict) > 0 and len(auc_val_dict) > 0:
                if "all" in fpr_dict:
                    plt.figure()
                    fpr, tpr, auc_val = fpr_dict["all"], tpr_dict["all"], auc_val_dict["all"]
                    plt.title(f"Receiver Operating Characteristic (Target {i + 1})")
                    plt.plot(fpr, tpr, "b", label=f"AUC = {auc_val:0.2F}")
                    plt.legend(loc="lower right")
                    plt.plot([0, 1], [0, 1], "k--")
                    plt.xlim([0, 1])
                    plt.ylim([0, 1])
                    plt.ylabel("True Positive Rate")
                    plt.xlabel("False Positive Rate")
                    plt.show()
                elif "micro" in fpr_dict:
                    micro_fpr, macro_fpr = fpr_dict.pop("micro"), fpr_dict.pop("macro")
                    micro_tpr, macro_tpr = tpr_dict.pop("micro"), tpr_dict.pop("macro")
                    micro_auc, macro_auc = auc_val_dict.pop("micro"), auc_val_dict.pop("macro")

                    classes = list(fpr_dict.keys())
                    classes_to_report = classes
                    if target_class is not None:
                        if target_class not in classes:
                            raise ValueError(f"'{target_class}' is not found in target classes")
                        classes_to_report = [target_class]
                    for _cls in classes_to_report:
                        plt.figure()
                        plt.title(f"ROC Class of '{_cls}' (Target {i + 1})")
                        plt.plot(micro_fpr, micro_tpr, label=f"micro-average ROC curve (area={micro_auc:0.2F})",
                                 color="deeppink", linestyle=":", linewidth=4)
                        plt.plot(macro_fpr, macro_tpr, "r",
                                 label=f"macro-average ROC curve (area={macro_auc:0.2F})",
                                 color="navy", linestyle=":", linewidth=4)
                        plt.plot(fpr_dict[_cls], tpr_dict[_cls], color="orange",
                                 label=f"ROC curve of class '{_cls}' (area={auc_val_dict[_cls]:0.2F})")
                        plt.legend(loc="lower right")
                        plt.plot([0, 1], [0, 1], "k--")
                        plt.xlim([0, 1])
                        plt.ylim([0, 1])
                        plt.ylabel("True Positive Rate")
                        plt.xlabel("False Positive Rate")
                        plt.show()

    @classmethod
    def generate_coarse_class_dashboard(cls, afe_report: BaseAfeOutputReport, feature_name: str):
        """Creates bar plot showing transformation map corresponding to given feature"""
        fig, ax = plt.subplots()
        fig.canvas.manager.set_window_title("Coarse Class Dashboard")
        cls.__get_coarse_class_bar_chart(afe_report, feature_name, ax)
        ax.set_xlabel("Range")
        ax.set_ylabel("Value")
        ax.set_title("Transformation Map")
        fig.autofmt_xdate()

        # PLOT LINE ON BAR PLOT WITH MATPLOTLIB (ileride kullanılacak)
        # pylint: disable=pointless-string-statement
        """
        _map = afe_report.transformations[feature_name].tabulate_as_text()
        map_vals = [float(i) for i in list(_map.values())]
        keys = list(_map.keys())
        ax2 = ax.twinx()
        ax2.plot(keys,[i for i,v in enumerate(keys)],label="target", color="orange")
        plt.legend()
        """

        fig.tight_layout()
        plt.show()
        return fig

    @classmethod
    def generate_memory_usage_dashboard(cls, afe_report: BaseAfeOutputReport):
        """Creates a line-scatter plot of memory usage by date"""
        fig, ax = plt.subplots()
        fig.canvas.manager.set_window_title("Memory Usage Dashboard")
        ax.set_title("Memory Usage")
        cls.__get_memory_usage_scatter(afe_report, ax)
        cls.__add_event_lines_to_ax(afe_report, ax)
        fig.autofmt_xdate()
        dashboard_helper.set_date_ticker(ax)
        plt.show()

    @classmethod
    def generate_cpu_usage_dashboard(cls, afe_report: BaseAfeOutputReport):
        """Creates a line-scatter plot of cpu usage by date"""
        fig, ax = plt.subplots()
        fig.canvas.manager.set_window_title("CPU Usage Dashboard")
        ax.set_title("CPU Usage")
        cls.__get_cpu_usage_scatter(afe_report, ax)
        cls.__add_event_lines_to_ax(afe_report, ax, for_cpu=True)
        # fig = create_figure([scatter], "CPU Usage", "Date", "Usage")
        # fig.show()
        fig.autofmt_xdate()
        dashboard_helper.set_date_ticker(ax)
        plt.show()

    @classmethod
    def __get_resource_usage_ax(cls, afe_report, ax):
        line1 = cls.__get_memory_usage_scatter(afe_report, ax)[0]

        color = "tab:blue"
        ax.set_ylabel("Memory Usage(MB)", color=color)
        ax.tick_params(axis='y', labelcolor=color)

        ax2 = ax.twinx()
        color2 = "tab:red"
        ax2.set_ylabel("CPU Usage(percentage)", color=color2)
        ax2.tick_params(axis='y', labelcolor=color2)
        line2 = cls.__get_cpu_usage_scatter(afe_report, ax2, color=color2)[0]
        cls.__add_event_lines_to_ax(afe_report, ax)
        ax.set_title("Resource Usage")
        return [line1, line2]

    @classmethod
    def generate_resource_usage_dashboard(cls, afe_report: BaseAfeOutputReport):
        """Creates a line-scatter plots of memory and cpu usages by date"""
        fig, ax = plt.subplots()
        lines = cls.__get_resource_usage_ax(afe_report, ax)
        fig.canvas.manager.set_window_title('Resource Usage Dashboard')
        fig.autofmt_xdate()
        dashboard_helper.set_date_ticker(ax)
        plt.legend(lines, [line.get_label() for line in lines])
        plt.show()

    @classmethod
    def __get_coarse_class_bar_chart(cls, afe_report: BaseAfeOutputReport, feature_name: str, ax: Axes) -> BarContainer:
        """Returns a matplotlib BarContainer object generated for afe transformation map of given feature"""
        _map = afe_report.transformations[feature_name].tabulate_as_text()
        limits = list(_map.keys())
        map_vals = [float(i) for i in list(_map.values())]

        bar_chart = dashboard_helper.get_bar_chart(limits, map_vals, "Observation Ratio", ax)

        return bar_chart

    @classmethod
    def __get_afe_feature_table(cls, report_helper_type: Type[ReportHelperType],
                                afe_report: BaseAfeOutputReport, ax: Axes, rows_per_page=10) -> TablePagination:
        """Returns a paginated table storing afe output features information"""
        data_frame = report_helper_type.get_output_features_as_data_frame(afe_report)
        table = dashboard_helper.get_data_table_plot(data_frame, ax, rows_per_page=rows_per_page)

        return table

    @classmethod
    def __get_memory_usage_scatter(cls, afe_report: BaseAfeOutputReport, ax: Axes) -> Line2D:
        """Returns a matplotlib Line2D object generated for memory usage by date"""
        usage = afe_report.memory_usage
        return dashboard_helper.get_line_scatter_plot(list(usage.keys()), list(usage.values()), "Memory Usage", ax)

    @classmethod
    def __get_cpu_usage_scatter(cls, afe_report: BaseAfeOutputReport, ax: Axes, color=None) -> Line2D:
        """Returns a matplotlib Line2D object generated for cpu usage by date"""
        usage = afe_report.cpu_usage
        return dashboard_helper.get_line_scatter_plot(list(usage.keys()), list(usage.values()), "CPU Usage", ax,
                                                      color=color)

    @classmethod
    def __add_event_lines_to_ax(cls, afe_report, ax: Axes, for_cpu=False):
        """Adds vertical lines for events in plot"""
        tick_vals = list(afe_report.event_times.values())
        tick_texts = list(afe_report.event_times.keys())
        values_dict = afe_report.memory_usage
        if for_cpu:
            values_dict = afe_report.cpu_usage
        max_val = max(values_dict.values())
        min_val = min(values_dict.values())
        total_time = max(values_dict.keys()) - min(values_dict.keys())
        for i, val in enumerate(tick_vals):
            if i < len(tick_vals) - 1:
                if (tick_vals[i + 1] - val).total_seconds() < total_time.total_seconds() / 100:
                    # prevents annotation overlapping by eliminating steps with a low execution time
                    continue
            ax.axvline(val, color="green", linestyle="--")
            ax.text(val + timedelta(seconds=0.1), (min_val + max_val) / 2, tick_texts[i], rotation=90,
                    color="green",
                    fontweight="bold", zorder=10, va="center")

    @classmethod
    def __convert_to_df(cls, count_dict: dict, property_name: str):
        new_dict = {property_name: [], "Count": []}
        for key, value in count_dict.items():
            new_dict[property_name].append(key)
            new_dict["Count"].append(value)
        return pd.DataFrame(new_dict)
