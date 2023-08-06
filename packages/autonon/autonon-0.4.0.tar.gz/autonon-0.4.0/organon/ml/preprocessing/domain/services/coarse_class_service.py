"""Includes CoarseClassService class"""
from typing import Union, Tuple

import numpy as np
import pandas as pd

from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.fl.core.helpers.data_frame_helper import get_column_native_type
from organon.fl.logging.helpers.log_helper import LogHelper
from organon.ml.common.enums.target_type import TargetType
from organon.ml.common.helpers.df_ops_helper import get_train_test_split_from_strata, get_sample_indices_from_series
from organon.ml.preprocessing.domain.objects.coarse_class_fit_output import CoarseClassFitOutput
from organon.ml.preprocessing.helpers.preprocessing_input_helper import convert_str_series_to_binary
from organon.ml.preprocessing.settings.objects.coarse_class_settings import CoarseClassSettings


class CoarseClassService:
    """Service for CoarseClass conversion"""

    def __init__(self, settings: CoarseClassSettings):
        if settings.target_type not in [TargetType.SCALAR, TargetType.BINARY]:
            raise ValueError("Target type should be scalar or binary.")
        self.settings = settings
        self.fit_output: CoarseClassFitOutput = None

    def fit(self, data: pd.DataFrame, target_data: pd.Series, stability_check_data: pd.DataFrame = None,
            stability_check_target_data: pd.Series = None) -> CoarseClassFitOutput:
        """fits coarse column and outputs coarse tables"""
        self._validate_data(data, target_data, stability_check_target_data, stability_check_target_data)
        target_native_type = get_column_native_type(pd.DataFrame({"target": target_data}), "target")
        if self.settings.target_type == TargetType.SCALAR and target_native_type != ColumnNativeType.Numeric:
            raise ValueError("Target column should be numeric for categorical coarse classing.")
        target_data, stability_check_target_data = self._check_target_data(target_data, stability_check_target_data,
                                                                           target_native_type)
        x_train, y_train, x_valid, y_valid = self._prepare_train_and_validation_data(data, target_data,
                                                                                     stability_check_data,
                                                                                     stability_check_target_data)
        fit_output = self._initialize_output(y_train)
        for col in x_train.columns:
            column_type = get_column_native_type(x_train, col)
            fit_output = self._execute_coarsing_for_col(fit_output, column_type, col, x_train[col], y_train,
                                                        x_valid[col], y_valid)
        self.fit_output = fit_output
        return fit_output

    def _validate_data(self, data: pd.DataFrame, target_data: pd.Series, stability_check_data: pd.DataFrame = None,
                       stability_check_target_data: pd.Series = None):
        if data is None or data.empty:
            raise ValueError("Data cannot be empty or None.")
        if self.settings.target_type == TargetType.BINARY and target_data.nunique() > 2:
            raise ValueError("Target type is binary but target contains more than two classes.")
        if len(data) != len(target_data) or any(data.index != target_data.index):
            raise ValueError("Data and target indexes are different.")
        if self.settings.stability_check:
            if stability_check_data is not None and stability_check_target_data is not None:
                if len(stability_check_data) != len(stability_check_target_data) or \
                        any(stability_check_data.index != stability_check_target_data.index):
                    raise ValueError("Stability check data and target data indexes are different.")

    def _check_target_data(self, target_data: pd.Series, stability_check_target_data: pd.Series,
                           target_native_type: ColumnNativeType):
        change_valid_data = False
        if self.settings.target_type == TargetType.BINARY and target_native_type != ColumnNativeType.Numeric:
            if self.settings.stability_check and (stability_check_target_data is not None):
                valid_target_type = get_column_native_type(pd.DataFrame(data=stability_check_target_data,
                                                                        columns=["target"]), "target")
                if valid_target_type == ColumnNativeType.Numeric:
                    raise ValueError("Target data includes non-numeric values but "
                                     "stability check data includes numeric values")
                change_valid_data = True
            if self.settings.positive_class is None or self.settings.negative_class is None:
                raise ValueError("Target includes non-numeric values but positive and negative classes are not given.")
            if change_valid_data:
                stability_check_target_data = convert_str_series_to_binary(
                    stability_check_target_data, self.settings.positive_class, self.settings.negative_class)
            target_data = convert_str_series_to_binary(target_data, self.settings.positive_class,
                                                       self.settings.negative_class)
        return target_data, stability_check_target_data

    def _execute_coarsing_for_col(self, fit_output: CoarseClassFitOutput, column_type: ColumnNativeType, col: str,
                                  x_train: pd.Series, y_train: pd.Series, x_valid: pd.Series, y_valid: pd.Series):
        # pylint: disable=too-many-arguments
        if x_train.nunique() <= 1:
            LogHelper.info(f"{col} cannot be coarse classed. Because it consists of a single value.")
            fit_output.rejected_list.append(col)
            return fit_output
        if column_type in [ColumnNativeType.Numeric, ColumnNativeType.String]:
            dt_df, x_val_tmp, y_val_tmp, null_char_table, null_cc_table, char_df = \
                self._summarize_column(x_train, y_train, x_valid, y_valid, col, column_type)
            if self._check_has_at_least_two_classes(dt_df):
                dt_df = self._coarse_column(dt_df, char_df, column_type, x_val_tmp, y_val_tmp,
                                            fit_output.target_mean)
                # if no stability check is desired then we are done here
                # continue for stability check
                if self.settings.stability_check:
                    dt_df = CoarseClassService._execute_stability(dt_df, self.settings.stability_threshold,
                                                                  column_type,
                                                                  fit_output.target_mean)
                fit_output.coarse_class_table = pd.concat([fit_output.coarse_class_table, dt_df, null_cc_table]
                                                          , ignore_index=True)
                fit_output.coarse_class_table["class_target_mean"].fillna(fit_output.target_mean, inplace=True)
                fit_output.char_table = pd.concat([fit_output.char_table, char_df, null_char_table],
                                                  ignore_index=True)
            else:
                LogHelper.info(f"{col} cannot be coarse classed.")
                fit_output.rejected_list.append(col)
        else:
            LogHelper.info(f"{col} cannot be coarse classed because its type is not numeric or object.")
            fit_output.rejected_list.append(col)
        return fit_output

    @staticmethod
    def _initialize_output(y_train: pd.Series) -> CoarseClassFitOutput:
        fit_output = CoarseClassFitOutput()
        fit_output.coarse_class_table = pd.DataFrame()
        fit_output.rejected_list = []
        fit_output.char_table = pd.DataFrame()
        # Save target mean and count
        fit_output.target_mean = y_train.mean()
        return fit_output

    @staticmethod
    def _check_has_at_least_two_classes(data_frame: pd.DataFrame) -> bool:
        return data_frame[data_frame['class_count'] > 0].shape[0] > 1

    def _summarize_column(self, x_train: pd.Series, y_train: pd.Series, x_valid: pd.Series,
                          y_valid: pd.Series, col: str, column_type: ColumnNativeType):
        x_tmp, y_tmp, x_val_tmp, y_val_tmp, y_nulls, y_valid_nulls = self._get_column_dfs(x_train,
                                                                                          y_train,
                                                                                          x_valid,
                                                                                          y_valid)
        null_char_table, null_cc_table = self._fill_cc_table_for_nulls(y_nulls, y_valid_nulls, col,
                                                                       y_train.mean(), y_train.count())
        char_df = pd.DataFrame()
        # convert categorical columns to numeric by assigning their target mean
        if column_type == ColumnNativeType.String:
            char_df, x_tmp = self._convert_categorical_col_to_numeric(x_tmp, col, y_tmp)
        # Build decision trees
        dt_df = self._build_decision_tree_df(self.settings.target_type, self.settings.min_class_size,
                                             self.settings.max_leaf_nodes, x_tmp, y_tmp, col)
        del x_tmp
        # Prepare coarse class summary table
        dt_df = self._prepare_cc_summary(dt_df, y_tmp, col, y_train.count())
        return dt_df, x_val_tmp, y_val_tmp, null_char_table, null_cc_table, char_df

    def _prepare_train_and_validation_data(self, x_train: pd.DataFrame, y_train: pd.Series,
                                           stability_check_data: pd.DataFrame, stability_target_data: pd.Series) \
            -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
        """prepares train and validation data sets"""
        # Get validation data for stability check
        if self.settings.stability_check:
            if stability_check_data is None:
                x_train, y_train, x_valid, y_valid = get_train_test_split_from_strata(x_train,
                                                                                      y_train,
                                                                                      self.settings.test_ratio,
                                                                                      self.settings.random_state)
            else:
                y_valid = stability_target_data
                x_valid = stability_check_data
        else:
            valid_indices = get_sample_indices_from_series(y_train, self.settings.test_ratio,
                                                           self.settings.random_state)
            x_valid, y_valid = x_train.loc[valid_indices], y_train.loc[valid_indices]
        return x_train, y_train, x_valid, y_valid

    @staticmethod
    def _get_column_dfs(x_train: pd.Series, y_train: pd.Series, x_valid: pd.Series, y_valid: pd.Series) -> Tuple[
        pd.Series, pd.Series, pd.Series, pd.Series, pd.Series, pd.Series]:
        y_nulls = y_train.loc[y_train.index.isin(x_train[x_train.isnull()].index)]
        y_valid_nulls = y_valid.loc[y_valid.index.isin(x_valid[x_valid.isnull()].index)]
        return x_train.dropna(), y_train.loc[y_train.index.isin(x_train.dropna().index)], \
               x_valid.dropna(), y_valid.loc[
                   y_valid.index.isin(x_valid.dropna().index)], y_nulls, y_valid_nulls

    @staticmethod
    def _fill_cc_table_for_nulls(y_nulls: pd.Series, y_valid_nulls: pd.Series, col, target_mean: float,
                                 class_count: int):
        y_null_mean = y_nulls.mean() if len(y_nulls) > 0 else float("nan")
        null_char_table = pd.DataFrame(
            {"char_value": ["NULL"],
             "num_value": [y_null_mean],
             "variable": [col]})
        null_char_table["num_value"].fillna(target_mean, inplace=True)
        null_cc_table = pd.DataFrame(
            {"class_min": [y_nulls.min()], "class_max": [y_nulls.max()], "class_count": [y_nulls.count()],
             "class_target_mean": [y_null_mean], "class_target_count": [y_nulls.sum()],
             "class_no": ["nulls"], "class_percent": [y_nulls.count() / class_count],
             "class_target_deviation": [
                 (y_null_mean - target_mean) / target_mean],
             "variable": [col], "class": ["null"],
             "class_count (val)": [y_valid_nulls.count()], "class_target_mean (val)": [y_valid_nulls.mean()],
             "class_target_count (val)": [y_valid_nulls.sum()],
             "unstability": [np.nan]})
        null_cc_table["class_target_mean"].fillna(target_mean, inplace=True)
        null_cc_table["class_target_mean (val)"].fillna(target_mean, inplace=True)
        return null_char_table, null_cc_table

    @staticmethod
    def _convert_categorical_col_to_numeric(x_train: pd.Series, column_name: str, y_train: pd.Series
                                            ) -> Tuple[pd.DataFrame, pd.Series]:
        """converts categorical columns to numeric columns"""
        data = pd.DataFrame(columns=[column_name, 'target'])
        data[column_name] = x_train
        data["target"] = y_train
        char_df = data.groupby(column_name).agg({"target": np.mean})
        char_df.reset_index(inplace=True)
        char_df.columns = [column_name, column_name + '_num']
        data['indexcol'] = data.index
        data = pd.merge(data, char_df, how='left', on=column_name, copy=False)
        data = data.drop([column_name, "target"], axis=1).rename(
            columns={column_name + '_num': column_name})
        data.set_index('indexcol', inplace=True)
        char_df.columns = ['char_value', 'num_value']
        char_df["num_value"] = char_df["num_value"]
        char_df['variable'] = column_name
        return char_df, data[column_name]

    @staticmethod
    def _build_decision_tree_df(target_type: TargetType, min_class_size: int, max_leaf_nodes: int,
                                x_fit_all: pd.Series, y_fit: pd.Series, column_name: str) -> pd.DataFrame:
        dt_df = pd.DataFrame(columns=[column_name, 'dt'])
        dt_df[column_name] = x_fit_all
        if target_type == TargetType.BINARY:
            from sklearn.tree import DecisionTreeClassifier  # pylint: disable=import-outside-toplevel
            dt_classifier = DecisionTreeClassifier(min_samples_leaf=min_class_size,
                                                   max_leaf_nodes=max_leaf_nodes)
            dt_classifier.fit(x_fit_all.values.reshape(-1, 1), y_fit.values.reshape(-1, 1))
            dt_df["dt"] = dt_classifier.predict_proba(x_fit_all.values.reshape(-1, 1))[:, 1]
        elif target_type == TargetType.SCALAR:
            from sklearn.tree import DecisionTreeRegressor  # pylint: disable=import-outside-toplevel
            dt_regressor = DecisionTreeRegressor(min_samples_leaf=min_class_size,
                                                 max_leaf_nodes=max_leaf_nodes)
            dt_regressor.fit(x_fit_all.values.reshape(-1, 1), y_fit.values.reshape(-1, 1))
            dt_df["dt"] = dt_regressor.predict(x_fit_all.values.reshape(-1, 1))
        return dt_df

    def _prepare_cc_summary(self, dt_df: pd.DataFrame, y_train: pd.Series,
                            column_name: str, class_count: int) -> pd.DataFrame:
        dt_df = self._prepare_cc_parameters_df(dt_df, y_train, column_name)
        dt_df.sort_values(by='class_min', inplace=True)
        dt_df.reset_index(inplace=True)
        dt_df['class_no'] = np.where(dt_df['class_min'].isnull(), 'nulls', dt_df.index + 1)
        dt_df['class_percent'] = dt_df['class_count'] / class_count
        dt_df['class_target_deviation'] = (dt_df['class_target_mean'] - y_train.mean()) / y_train.mean()
        dt_df['variable'] = column_name
        del dt_df["dt"]
        return dt_df

    def _prepare_cc_parameters_df(self, dt_df: pd.DataFrame, y_train: pd.Series, column_name: str) -> pd.DataFrame:
        dt_df_base = dt_df.copy()
        dt_df_base["target"] = y_train
        dt_df = self._prepare_class_statistics(dt_df_base, column_name)
        # if class boundaries overlap, then class intervals are reconstructed.
        while self._check_class_overlap(dt_df):
            min_value = dt_df[dt_df['lag'] < dt_df['class_max']]['lag'].values[0]
            dt_value = dt_df[dt_df['lag'] == min_value].index.values[0]
            dt_df_base.loc[(dt_df_base[column_name] > min_value) & (dt_df_base['dt'] == dt_value),
                           "dt"] = dt_df_base['dt'] + 0.0000000001
            dt_df = self._prepare_class_statistics(dt_df_base, column_name)
        dt_df["class_max"] = dt_df["class_min"].shift(-1)
        dt_df.loc[dt_df.index[-1], "class_max"] = np.inf
        dt_df.drop('lag', axis=1, inplace=True)
        return dt_df

    @staticmethod
    def _check_class_overlap(dt_df: pd.DataFrame):
        return dt_df[dt_df['lag'] < dt_df['class_max']]['lag'].count() > 0

    @staticmethod
    def _prepare_class_statistics(dt_df_base: pd.DataFrame, column_name: str) -> pd.DataFrame:
        dt_df = dt_df_base.groupby('dt').agg({column_name: [min, max, 'count'], "target": [np.mean, sum]})
        dt_df.columns = ['class_min', 'class_max', 'class_count', 'class_target_mean', 'class_target_count']
        dt_df.sort_values(by='class_min', inplace=True)
        dt_df['lag'] = dt_df['class_min'].shift(-1)
        return dt_df

    def _coarse_column(self, dt_df: pd.DataFrame, char_df: pd.DataFrame,
                       column_type: ColumnNativeType,
                       x_valid: pd.Series, y_valid: pd.Series,
                       target_mean: Union[float, int]) -> pd.DataFrame:
        # pylint: disable=too-many-arguments
        dt_df = self._get_categorical_class_parameters(dt_df, column_type, char_df)
        # first calculate class count, class target count and class target mean for validation data
        # it is done separately for numeric and non-numeric columns
        if column_type == ColumnNativeType.Numeric:
            dt_df_val = CoarseClassService._calculate_validation_parameters_numeric(dt_df, x_valid, y_valid)
        else:
            dt_df_val = CoarseClassService._calculate_validation_parameters_object(dt_df, x_valid, y_valid)
        dt_df_val.loc[dt_df_val['class_target_mean (val)'].isnull(), 'class_target_mean (val)'] = target_mean
        dt_df = pd.merge(dt_df, dt_df_val, how='left', on='class_no', copy=False)
        return dt_df

    @staticmethod
    def _get_categorical_class_parameters(dt_df: pd.DataFrame, column_type: ColumnNativeType,
                                          char_df: pd.DataFrame) -> pd.DataFrame:
        dt_df['class'] = round(dt_df['class_min'], 3).astype(str) + '-' + round(dt_df['class_max'], 3).astype(
            str)
        # if column is categorical, then find which class it belongs to and append category to its "class" field.
        if column_type == ColumnNativeType.String:
            char_df['dummy'] = 1
            dt_df['dummy'] = 1
            df_tmp = pd.merge(char_df, dt_df[['class_min', 'class_max', 'class', 'dummy']], how='outer',
                              on='dummy', copy=False)
            char_df.drop('dummy', axis=1, inplace=True)
            dt_df.drop('dummy', axis=1, inplace=True)
            df_tmp = df_tmp[
                (df_tmp['num_value'] >= df_tmp['class_min']) & (df_tmp['num_value'] < df_tmp['class_max'])]
            dt_df = pd.merge(dt_df, pd.DataFrame(
                df_tmp.groupby(['class'])['char_value'].apply(','.join)).reset_index(), on='class', copy=False).drop(
                'class', axis=1).rename(columns={'char_value': 'class'})
        return dt_df

    @classmethod
    def _calculate_validation_parameters_numeric(cls, dt_df: pd.DataFrame, x_valid: pd.Series,
                                                 y_valid: pd.Series) -> pd.DataFrame:
        # pylint: disable=cell-var-from-loop
        dt_df_val = dt_df[['class_no', 'class_count', 'class_target_mean', 'class_target_count']]
        dt_df_val.columns = ['class_no', 'class_count (val)', 'class_target_mean (val)',
                             'class_target_count (val)']
        for class_no in dt_df["class_no"]:
            minn = dt_df[dt_df["class_no"] == class_no]["class_min"].values[0]
            maxx = dt_df[dt_df["class_no"] == class_no]["class_max"].values[0]
            target_values = y_valid[
                y_valid.index.isin(x_valid.where(lambda x: (x >= minn) & (x < maxx)).dropna().index)]
            class_count = target_values.count()
            class_mean = target_values.mean()
            class_sum = target_values.sum()
            dt_df_val.loc[dt_df_val['class_no'] == class_no, 'class_count (val)'] = class_count
            dt_df_val.loc[dt_df_val['class_no'] == class_no, 'class_target_mean (val)'] = class_mean
            dt_df_val.loc[dt_df_val['class_no'] == class_no, 'class_target_count (val)'] = class_sum
        return dt_df_val

    @classmethod
    def _calculate_validation_parameters_object(cls, dt_df: pd.DataFrame, x_valid: pd.Series,
                                                y_valid: pd.Series) -> pd.DataFrame:
        x_valid.fillna('NULL', inplace=True)
        dt_df_val = dt_df[['class_no', 'class_count', 'class_target_mean', 'class_target_count']]
        dt_df_val.columns = ['class_no', 'class_count (val)', 'class_target_mean (val)',
                             'class_target_count (val)']
        for class_no in dt_df["class_no"].values:
            value_list = dt_df[dt_df['class_no'] == class_no]['class'].values[0].split(",")
            dt_df_val.loc[dt_df_val['class_no'] == class_no, 'class_count (val)'] = \
                x_valid[x_valid.isin(value_list)].count()
            dt_df_val.loc[dt_df_val['class_no'] == class_no, 'class_target_mean (val)'] = y_valid[
                y_valid.index.isin(x_valid[x_valid.isin(value_list)].index)].mean()
            dt_df_val.loc[dt_df_val['class_no'] == class_no, 'class_target_count (val)'] = y_valid[
                y_valid.index.isin(x_valid[x_valid.isin(value_list)].index)].sum()
        return dt_df_val

    @staticmethod
    def _assign_unstability(dt_df: pd.DataFrame) -> pd.DataFrame:
        dt_df['unstability'] = np.where(dt_df['class_target_mean'] != 0.0,
                                        round(abs(dt_df['class_target_mean'] - dt_df['class_target_mean (val)']) / (
                                                dt_df['class_target_mean'] + 0.0000000001), 2), 1.0)
        dt_df['unstability'] = np.where((dt_df['class_target_mean'] == 0.0) & (dt_df["class_target_mean (val)"] == 0.0),
                                        0, dt_df['unstability'])
        return dt_df

    @classmethod
    def _execute_stability(cls, dt_df: pd.DataFrame, stability_threshold: float,
                           column_type: ColumnNativeType,
                           target_mean: float) -> pd.DataFrame:
        dt_df = cls._assign_unstability(dt_df)
        # Loop until there is no unstable class
        while dt_df[dt_df['unstability'] > stability_threshold]['class_no'].count() > 0 and len(dt_df["class_no"]) > 1:
            max_class_no = dt_df['class_no'].astype(int).max()
            unstable_class, combine_class = cls._get_unstable_and_combine_class(dt_df, stability_threshold, column_type,
                                                                                max_class_no)
            # combine two classes
            combined_row = cls._combine_two_classes(dt_df, unstable_class, combine_class, target_mean)
            dt_df = dt_df[~dt_df['class_no'].isin([str(unstable_class), str(combine_class)])]
            dt_df = pd.concat([dt_df, combined_row])
            dt_df.sort_values(by='class_min', inplace=True)
            dt_df.reset_index(inplace=True, drop=True)
            dt_df['class_no'] = np.where(dt_df['class_no'] == 'nulls', 'nulls', dt_df.index + 1)
        return dt_df

    @staticmethod
    def _get_unstable_and_combine_class(dt_df: pd.DataFrame, stability_threshold: float, column_type: ColumnNativeType,
                                        max_class_no: int) -> Tuple[int, int]:
        unstable_class = dt_df[(dt_df['unstability'] > stability_threshold)][
            'class_no'].astype(int).min()
        # for numeric columns unstable classes are combined with their adjacent classes
        if column_type == ColumnNativeType.Numeric:
            if unstable_class == 1:
                combine_class = unstable_class + 1
            elif unstable_class == max_class_no:
                combine_class = unstable_class - 1
            else:
                t_mean = dt_df[dt_df['class_no'] == str(unstable_class)]['class_target_mean'].values[0]
                next_mean = \
                    dt_df[dt_df['class_no'] == str(unstable_class + 1)]['class_target_mean'].values[0]
                prev_mean = \
                    dt_df[dt_df['class_no'] == str(unstable_class - 1)]['class_target_mean'].values[0]
                if abs(t_mean - next_mean) <= abs(t_mean - prev_mean):
                    combine_class = unstable_class + 1
                else:
                    combine_class = unstable_class - 1
        # for non-numeric columns, an unstable class is combined with the one having the closes target mean
        else:
            unstable_class_mean = \
                dt_df[dt_df['class_no'] == str(unstable_class)]['class_target_mean'].values[0]
            min_difference = abs(dt_df[dt_df['class_no'] != str(unstable_class)][
                                     'class_target_mean'] - unstable_class_mean).min()
            dt_df['difference'] = abs(dt_df['class_target_mean'] - unstable_class_mean)
            combine_class = int(
                dt_df[dt_df['difference'] == min_difference]['class_no'].values[0])
            dt_df.drop('difference', axis=1, inplace=True)
        return unstable_class, combine_class

    @staticmethod
    def _combine_two_classes(dt_df: pd.DataFrame, unstable_class: int, combine_class: int,
                             target_mean: float) -> pd.DataFrame:
        unstable_row = dt_df[dt_df['class_no'] == str(unstable_class)]
        combine_row = dt_df[dt_df['class_no'] == str(combine_class)]
        combined_row = pd.concat([unstable_row, combine_row])
        new_row = combined_row.groupby('variable').agg({'class_min': min,
                                                        'class_max': max,
                                                        'class_count': sum,
                                                        'class_target_count': sum,
                                                        'class_no': min,
                                                        'class_percent': sum,
                                                        'class_count (val)': sum,
                                                        'class_target_count (val)': sum})
        new_row = pd.concat(
            [new_row, pd.DataFrame(combined_row.groupby(['variable'])['class'].apply(','.join))],
            axis=1)
        new_row['class_no'] = new_row['class_no'].astype(str)
        new_row['class_target_mean'] = new_row['class_target_count'] / new_row['class_count']
        new_row['class_target_mean (val)'] = new_row['class_target_count (val)'] / new_row[
            'class_count (val)']
        new_row['class_target_mean (val)'].fillna(target_mean, inplace=True)
        new_row.reset_index(inplace=True)
        new_row['class_target_deviation'] = (new_row['class_target_mean'] - target_mean) / target_mean
        CoarseClassService._assign_unstability(new_row)
        new_row = new_row[unstable_row.columns]
        return new_row

    def transform(self, data: pd.DataFrame, with_class_value=False):
        """transforms data"""
        if self.fit_output is None:
            raise ValueError("You should call fit method first to transform data.")
        base_df = data.drop(data.columns, axis=1)
        for col in data.columns:
            transformed_col_name = "Z_" + str(col)
            class_value_col_name = "C_" + str(col)
            column_type = get_column_native_type(data, col)
            if col not in self.fit_output.rejected_list:
                x_df = data[col]
                c_series_base = data[col]
                c_df = pd.DataFrame()
                c_df["C_col"] = x_df
                cc_table = self.fit_output.coarse_class_table[self.fit_output.coarse_class_table['variable'] == col]
                if column_type == ColumnNativeType.Numeric:
                    x_df, c_df = self._fill_outliers(x_df, c_series_base, c_df, cc_table, with_class_value)
                    x_df, c_df = self._fill_nulls(x_df, c_series_base, c_df, cc_table, with_class_value)
                    x_df, c_df = self._fill_for_not_objects(x_df, c_series_base, c_df, cc_table, with_class_value)
                else:
                    x_df, c_df = self._fill_for_objects(x_df, c_series_base, c_df, cc_table, with_class_value)
                base_df[transformed_col_name] = x_df
                if with_class_value:
                    base_df[class_value_col_name] = c_df["C_col"]
                del x_df
        return base_df

    def _fill_nulls(self, x_df: pd.Series, c_series: pd.Series, c_df: pd.DataFrame, cc_table: pd.DataFrame,
                    with_class_value: bool) -> Tuple[
        pd.Series, pd.DataFrame]:
        if with_class_value:
            c_df.loc[c_series.isnull(), "C_col"] = "null"
        return pd.Series(data=np.where(x_df.isnull(),
                                       cc_table[cc_table['class'] == "null"][
                                           'class_target_mean'] - self.fit_output.target_mean,
                                       x_df)), c_df

    @staticmethod
    def _fill_outliers(x_df: pd.Series, c_series: pd.Series, c_df: pd.DataFrame, cc_table: pd.DataFrame,
                       with_class_value: bool) -> Tuple[
        pd.Series, pd.DataFrame]:
        minn = cc_table[cc_table["class"] != "null"]['class_min'].min()
        maxx = np.inf if np.isinf(cc_table[cc_table["class"] != "null"]['class_max'].max()) else \
            cc_table[cc_table["class"] != "null"]['class_max'].max()
        x_df = np.where(x_df.notna() & ((x_df < minn) | (x_df >= maxx)), 0, x_df)
        if with_class_value:
            min_outlier_category = f"outlier_<{minn}"
            max_outlier_category = "outlier_>=inf" if np.isinf(maxx) else f"outlier_>={maxx}"
            c_df = pd.DataFrame(data=c_series.values, columns=["C_col"], index=c_series.index)
            c_df.loc[c_series.notna() & (c_series < minn), "C_col"] = min_outlier_category
            c_df.loc[c_series.notna() & (c_series >= maxx), "C_col"] = max_outlier_category
        return pd.Series(data=x_df), c_df

    def _fill_for_objects(self, x_df: pd.Series, c_series: pd.Series, c_df: pd.DataFrame, cc_table: pd.DataFrame,
                          with_class_value: bool) -> \
            Tuple[pd.Series, pd.DataFrame]:
        # unseed categories will remain zero
        res_df = pd.DataFrame(columns=["column", "transformed"])
        res_df["column"] = x_df
        res_df["transformed"] = 0
        categories = []
        for class_no in cc_table[cc_table["class"] != "null"]["class_no"]:
            res_df.loc[res_df["column"].isin(
                cc_table[cc_table['class_no'] == class_no]['class'].values[0].split(',')), "transformed"] = \
                cc_table[cc_table['class_no'] == class_no]['class_target_mean'].values[0] - \
                self.fit_output.target_mean
            if with_class_value:
                category = cc_table[cc_table['class_no'] == class_no]['class'].values[0]
                category_values = category.split(',')
                c_df.loc[c_df["C_col"].isin(category_values), "C_col"] = category
                categories.extend(category_values)
        res_df.loc[res_df["column"].isnull(), "transformed"] = \
            cc_table[cc_table['class'] == "null"]['class_target_mean'].values[0] - self.fit_output.target_mean
        if with_class_value:
            c_df.loc[c_series.notna() & ~c_series.isin(categories), "C_col"] = "Other (Unseen)"
            c_df.loc[c_series.isnull(), "C_col"] = "null"
        return res_df["transformed"], c_df

    def _fill_for_not_objects(self, x_df: pd.Series, c_series: pd.Series, c_df: pd.DataFrame, cc_table: pd.DataFrame,
                              with_class_value: bool) -> Tuple[pd.Series, pd.DataFrame]:
        for class_no in cc_table[cc_table["class"] != "null"]["class_no"]:
            minn = cc_table[cc_table["class_no"] == class_no]["class_min"].values[0]
            maxx = cc_table[cc_table["class_no"] == class_no]["class_max"].values[0]
            meann = cc_table[cc_table['class_no'] == class_no]['class_target_mean'].values[0]
            x_df = np.where((x_df >= minn) & (x_df < maxx), meann - self.fit_output.target_mean, x_df)
            if with_class_value:
                category = cc_table[cc_table["class_no"] == class_no]["class"].values[0]
                c_df.loc[((~c_series.isin([np.inf, -np.inf, np.nan])) & (c_series >= minn) & (
                        c_series < maxx)), "C_col"] = category
        return x_df, c_df
