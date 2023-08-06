"""Includes SamplingService class."""
from typing import List, Dict, Any, Tuple, TypeVar

import pandas as pd

from organon.fl.core.exceptionhandling.known_exception import KnownException
from organon.ml.common.helpers import df_ops_helper
from organon.ml.sampling.domain.objects.sampling_output import SamplingOutput
from organon.ml.sampling.domain.services.sampling_preprocessing_service import SamplingPreprocessingService
from organon.ml.sampling.settings.enums.sampling_strategy import SamplingStrategy
from organon.ml.sampling.settings.objects.sampling_settings import SamplingSettings

TargetClassValue = TypeVar("TargetClassValue")


# THIS CLASS IS OPTIMIZED FOR LOW PEAK MEMORY USAGE AND EXECUTION TIME.
# MEASURE PEAK MEMORY USAGE AND EXECUTION TIMES BEFORE AND AFTER DEVELOPMENT.

class SamplingService:
    """Sampling service"""

    @classmethod
    def sample(cls, sampling_settings: SamplingSettings) -> SamplingOutput:
        """Samples data according to given settings and returns sampled train data (and test data optionally)."""
        strata_cols = sampling_settings.strata_columns
        data = SamplingPreprocessingService.discretize(sampling_settings.data, strata_cols)

        if sampling_settings.split_test_data:
            x_train, x_test = df_ops_helper.get_train_test_split(data, sampling_settings.test_split_ratio,
                                                                 strata_columns=strata_cols)
        else:
            x_train = data
            x_test = None

        if sampling_settings.sampling_strategy == SamplingStrategy.UNDERSAMPLING:
            if sampling_settings.data_sample_ratio is not None:
                x_train = cls._get_random_sampled(x_train, sampling_settings.data_sample_ratio, strata_cols)

            x_train = cls._get_undersampled(x_train, sampling_settings.target_column_name,
                                            sampling_settings.sampling_ratio,
                                            strata_cols)
        elif sampling_settings.sampling_strategy == SamplingStrategy.OVERSAMPLING:
            if sampling_settings.data_sample_ratio is not None:
                x_train = cls._get_random_sampled(x_train, sampling_settings.data_sample_ratio, strata_cols)

            x_train = cls._get_oversampled(x_train, sampling_settings.target_column_name,
                                           sampling_settings.sampling_ratio,
                                           strata_cols)
        elif sampling_settings.sampling_strategy == SamplingStrategy.RANDOM_SAMPLING:
            x_train = cls._get_random_sampled(x_train, sampling_settings.sampling_ratio, strata_cols)

        output = SamplingOutput()
        output.train_data = x_train
        output.test_data = x_test
        return output

    @classmethod
    def _get_undersampled(cls, data: pd.DataFrame, target_column: str, sampling_ratio: float,
                          strata_columns: List[str]):
        target_value_counts: dict = data[target_column].value_counts(dropna=False).to_dict()
        target_classes = list(target_value_counts.keys())
        if len(target_classes) == 2:
            return cls._get_undersampled_for_binary_target(data, target_value_counts, target_column, sampling_ratio,
                                                           strata_columns)
        return cls._get_undersampled_for_multiclass_target(data, target_column, target_classes, target_value_counts,
                                                           strata_columns)

    @classmethod
    def _get_oversampled(cls, data: pd.DataFrame, target_column: str, sampling_ratio: float,
                         strata_columns: List[str]):
        target_value_counts: dict = data[target_column].value_counts(dropna=False).to_dict()
        target_classes = list(target_value_counts.keys())

        if len(target_classes) == 2:
            return cls._get_oversampled_for_binary_target(data, target_value_counts, target_column, sampling_ratio,
                                                          strata_columns)
        return cls._get_oversampled_for_multiclass_target(data, target_column, target_classes, target_value_counts,
                                                          strata_columns)

    @classmethod
    def _get_undersampled_for_binary_target(cls, data: pd.DataFrame, target_value_counts: Dict[Any, int],
                                            target_column: str,
                                            sampling_ratio: float, strata_columns: List[str]):
        min_freq_class, min_freq = cls._get_min_frequency_and_class(target_value_counts)
        expected_length_for_other = int(min_freq / sampling_ratio) - min_freq
        min_freq_class_rows = data[target_column] == min_freq_class

        df_min_class_indices = data.index[min_freq_class_rows]
        len_data = sum(target_value_counts.values())
        len_other = len_data - min_freq
        if expected_length_for_other > len_other:
            raise KnownException("Undersampling ratio cannot be less than the ratio of minimum sized class")
        if expected_length_for_other == len_other:
            return data
        df_other_indices = cls._get_sample_indices(cls._get_strata_columns(data[~min_freq_class_rows], strata_columns),
                                                   strata_columns,
                                                   expected_length_for_other / len_other)
        return data.loc[df_min_class_indices.tolist() + df_other_indices.tolist()]

    @classmethod
    def _get_undersampled_for_multiclass_target(cls, data: pd.DataFrame, target_column: str, target_classes: list,
                                                target_value_counts: Dict[Any, int], strata_columns: List[str]):
        min_freq_class, min_freq = cls._get_min_frequency_and_class(target_value_counts)
        min_freq_class_rows = data[target_column] == min_freq_class
        all_indices = data.index[min_freq_class_rows].tolist()
        for target_class in target_classes:
            if target_class == min_freq_class:
                continue
            target_class_size = target_value_counts[target_class]
            target_class_indices = cls._get_sample_indices(
                cls._get_strata_columns(data[data[target_column] == target_class], strata_columns),
                strata_columns, min_freq / target_class_size)
            all_indices.extend(target_class_indices)
        return data.loc[all_indices]

    @classmethod
    def _get_min_frequency_and_class(cls, target_value_counts: Dict[TargetClassValue,
                                                                    int]) -> Tuple[TargetClassValue, int]:
        min_freq = min(target_value_counts.values())
        min_freq_class = next(val for val, frequency in target_value_counts.items() if frequency == min_freq)
        return min_freq_class, min_freq

    @classmethod
    def _get_max_frequency_and_class(cls, target_value_counts: Dict[TargetClassValue,
                                                                    int]) -> Tuple[TargetClassValue, int]:
        max_freq = max(target_value_counts.values())
        max_freq_class = next(val for val, frequency in target_value_counts.items() if frequency == max_freq)
        return max_freq_class, max_freq

    @classmethod
    def _get_oversampled_for_binary_target(cls, data: pd.DataFrame, target_value_counts: Dict[Any, int],
                                           target_column: str, sampling_ratio: float, strata_columns: List[str]):
        max_freq_class, max_freq = cls._get_max_frequency_and_class(target_value_counts)
        max_freq_class_rows = data[target_column] == max_freq_class

        data_len = sum(target_value_counts.values())
        len_other = data_len - max_freq
        expected_length_for_other_class = int(max_freq / (1 - sampling_ratio) - max_freq)
        expected_ratio = expected_length_for_other_class / len_other

        df_max_class = data.index[max_freq_class_rows]
        if expected_ratio < 1:
            raise KnownException("Oversampling ratio cannot be less than the ratio of minimum sized class")
        if expected_ratio == 1:
            return data
        indices = cls._get_sample_indices(cls._get_strata_columns(data[~max_freq_class_rows], strata_columns),
                                          strata_columns, frac=expected_ratio, replace=True)
        return data.loc[df_max_class.tolist() + indices.tolist()]

    @classmethod
    def _get_oversampled_for_multiclass_target(cls, data: pd.DataFrame, target_column: str, target_classes: list,
                                               target_value_counts: Dict[Any, int], strata_columns: List[str]):
        max_freq_class, max_freq = cls._get_max_frequency_and_class(target_value_counts)
        max_freq_class_rows = data[target_column] == max_freq_class
        new_df_indices = data.index[max_freq_class_rows].tolist()
        for target_class in target_classes:
            if target_class == max_freq_class:
                continue
            len_df_class = target_value_counts[target_class]
            indices = cls._get_sample_indices(cls._get_strata_columns(data[data[target_column] == target_class],
                                                                      strata_columns), strata_columns,
                                              frac=max_freq / len_df_class, replace=True)
            new_df_indices.extend(indices)
        return data.loc[new_df_indices]

    @classmethod
    def _get_random_sampled(cls, data: pd.DataFrame, sampling_ratio: float,
                            strata_columns: List[str]):
        indices = cls._get_sample_indices(cls._get_strata_columns(data, strata_columns), strata_columns,
                                          sampling_ratio)
        return data.loc[indices]

    @classmethod
    def _get_sample_indices(cls, data: pd.DataFrame, strata_columns: List[str], frac: float, replace=False):
        return df_ops_helper.get_sample_indices(data, frac, strata_columns=strata_columns, replace=replace)

    @classmethod
    def _get_strata_columns(cls, data: pd.DataFrame, strata_columns: List[str]):
        if strata_columns is None:
            return None
        return data[strata_columns]
