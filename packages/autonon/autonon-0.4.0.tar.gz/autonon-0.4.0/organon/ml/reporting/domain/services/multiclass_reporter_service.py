"""Includes MulticlassReporterService class."""
from typing import List
import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_auc_score
from sklearn.preprocessing import label_binarize

from organon.ml.reporting.domain.objects.multiclass_report import MulticlassReport
from organon.ml.reporting.domain.services.base_reporter_service import BaseReporterService
from organon.ml.reporting.settings.objects.multiclass_reporter_settings import MultiClassReporterSettings


class MulticlassReporterService(BaseReporterService[MulticlassReport]):
    """Reporter service for multiclass classification"""

    def execute(self, settings: MultiClassReporterSettings) -> MulticlassReport:
        """returns multiclass report"""

        report = MulticlassReport()
        id_str_exists = settings.id_str_column is not None
        split_col_exists = settings.split_column is not None
        group_by_columns = []
        if id_str_exists:
            group_by_columns.append(settings.id_str_column)
        if split_col_exists:
            group_by_columns.append(settings.split_column)

        scores_table, confusion_matrix_dict, classification_report_dict = self._generate_reports(settings,
                                                                                                 id_str_exists,
                                                                                                 split_col_exists,
                                                                                                 group_by_columns)
        report.scores = scores_table
        report.confusion_matrices = confusion_matrix_dict
        report.classification_reports = classification_report_dict
        return report

    def _generate_reports(self, settings: MultiClassReporterSettings, id_str_exists: bool, split_col_exists: bool,
                          group_by_columns: List[str]):
        score_table_cols = self._initialize_acc_and_roc_table_cols(id_str_exists, split_col_exists,
                                                                               "Accuracy", "Roc-Auc Score")

        confusion_matrix_dict = {}
        classification_report_dict = {}
        roc_score = None
        scores_list = []
        score_column = settings.score_column if settings.probability_values is None else "Class Predicts"
        if settings.probability_values is not None:
            if settings.ordered_class_names is None:
                raise ValueError("When probability_values were given, ordered_class_names cannot be empty.")
            MulticlassReporterService._check_probability_values_data_length_match(settings)
            MulticlassReporterService._check_class_names_and_probability_values_match(settings)
            class_predicts = MulticlassReporterService._convert_probs_to_class_score(settings)
            settings.data["Class Predicts"] = class_predicts
        MulticlassReporterService._check_data_columns(settings, score_column)
        if group_by_columns:
            for groups, indices in settings.data.groupby(group_by_columns).indices.items():
                index_vals = list(set(list(settings.data.loc[indices][settings.target_column].unique()) +
                                      list(settings.data.loc[indices][score_column].unique())))
                index_vals.sort()
                group_tuple = groups if isinstance(groups, tuple) else (groups,)
                group_frame = settings.data.loc[indices]

                if settings.probability_values is not None:
                    roc_score = MulticlassReporterService._calculate_roc_auc_score(settings)

                confusion_matrix_dict[group_tuple] = pd.DataFrame(
                    data=confusion_matrix(group_frame[settings.target_column], group_frame[score_column],
                                          labels=index_vals), columns=index_vals, index=index_vals)
                classification_report_dict[group_tuple] = pd.DataFrame(
                    classification_report(group_frame[settings.target_column], group_frame[score_column],
                                          labels=index_vals, output_dict=True, zero_division=1)).transpose()

                acc_score = accuracy_score(group_frame[settings.target_column], group_frame[score_column])
                scores_list.append([*list(group_tuple), acc_score, roc_score])

            scores_df = pd.DataFrame(data=scores_list,
                                     columns=score_table_cols)

            if score_column == "Class Predicts":
                settings.data.drop(score_column, inplace=True, axis=1)

            return scores_df, confusion_matrix_dict, classification_report_dict

        index_vals = settings.data[settings.target_column].unique()

        if settings.probability_values is not None:
            roc_score = MulticlassReporterService._calculate_roc_auc_score(settings)

        confusion_matrix_dict[("ALL",)] = pd.DataFrame(
            data=confusion_matrix(settings.data[settings.target_column], settings.data[score_column],
                                  labels=index_vals), columns=index_vals, index=index_vals)
        classification_report_dict[("ALL",)] = pd.DataFrame(
            classification_report(settings.data[settings.target_column], settings.data[score_column],
                                  labels=index_vals, output_dict=True, zero_division=1)).transpose()

        scores_df = pd.DataFrame(data={"Accuracy": [accuracy_score(settings.data[settings.target_column],
                                                                   settings.data[score_column])],
                                       "Roc-Auc Score": [roc_score]})
        if score_column == "Class Predicts":
            settings.data.drop(score_column, inplace=True, axis=1)

        return scores_df, confusion_matrix_dict, classification_report_dict

    @staticmethod
    def _initialize_acc_and_roc_table_cols(id_str_exists: bool, split_col_exists: bool, acc_col: str, roc_col: str):
        columns = [acc_col, roc_col]
        if split_col_exists:
            columns.insert(0, "Data")
        if id_str_exists:
            columns.insert(0, "IdStr")
        return columns

    @staticmethod
    def _convert_probs_to_class_score(settings: MultiClassReporterSettings):
        """convert probability values to class predictions, and store proba values"""
        class_predictions = np.argmax(settings.probability_values, axis=1)
        arranged_class_predictions = []
        for class_name in class_predictions:
            arranged_class_name = settings.ordered_class_names.index(class_name)
            arranged_class_predictions.append(arranged_class_name)
        return pd.Series(arranged_class_predictions, index=settings.data.index)

    @staticmethod
    def _calculate_roc_auc_score(settings: MultiClassReporterSettings):
        """calculate roc auc score if predicted column has predict_proba values"""
        if len(np.unique(settings.data[settings.target_column])) > 1:
            y_test = label_binarize(settings.data[settings.target_column], classes=settings.ordered_class_names)
            scores = roc_auc_score(y_test, settings.probability_values, average='weighted',
                                   multi_class='ovr')
            return scores
        scores = None
        return scores

    @staticmethod
    def _check_data_columns(settings: MultiClassReporterSettings, score_column: str):
        """check if target and predicted columns includes string value if it does, raise error"""
        if not is_numeric_dtype(settings.data[settings.target_column]):
            raise ValueError("Target Column can only contain numeric values.")
        if not is_numeric_dtype(settings.data[score_column]):
            raise ValueError("Prediction Column can only contain numeric values.")

    @staticmethod
    def _check_class_names_and_probability_values_match(settings: MultiClassReporterSettings):
        """raise error if class order names array shape and prob values shapes mismatch"""
        if settings.probability_values is not None:
            num_classes = len(settings.ordered_class_names)
            if settings.probability_values.shape[1] != num_classes:
                raise ValueError("Given class names array shape mismatches with probability_values array.")

    @staticmethod
    def _check_probability_values_data_length_match(settings: MultiClassReporterSettings):
        """raise error if data target_column's length mismatches probability_values length"""
        if settings.probability_values is not None:
            if settings.probability_values.shape[0] != len(settings.data):
                raise ValueError("Given probability values mismatches with target column's length.")
