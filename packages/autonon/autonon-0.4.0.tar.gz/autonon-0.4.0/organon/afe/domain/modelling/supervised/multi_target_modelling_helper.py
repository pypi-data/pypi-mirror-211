"""Includes MultiTargetModellingHelper class."""
import contextlib
import random
from typing import List, Optional

import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier, LGBMRegressor
from sklearn.metrics import roc_curve, auc

from organon.afe.domain.enums.afe_operator import AfeOperator
from organon.afe.domain.enums.afe_target_column_type import AfeTargetColumnType
from organon.afe.domain.modelling.businessobjects.data_frame_builder import DataFrameBuilder
from organon.afe.domain.modelling.supervised.afe_supervised_algorithm_settings import AfeSupervisedAlgorithmSettings
from organon.afe.domain.modelling.supervised.multi_target_entity_container_service import \
    MultiTargetEntityContainerService
from organon.afe.domain.settings.base_afe_modelling_settings import BaseAfeModellingSettings
from organon.afe.domain.settings.model_settings import ModelSettings
from organon.afe.domain.settings.target_descriptor import TargetDescriptor
from organon.fl.core.businessobjects.dict_dataframe import DictDataFrame
from organon.fl.core.exceptionhandling.known_exception import KnownException
from organon.fl.core.businessobjects.data_partition import DataPartition
from organon.fl.core.businessobjects.idata_partition import IDataPartition
from organon.fl.logging.helpers.log_helper import LogHelper


class MultiTargetModellingHelper:
    """Helper class for MultiTarget modelling operations."""

    def __init__(self, settings: BaseAfeModellingSettings):
        self._settings = settings

    @staticmethod
    def get_partition(frame_builder: DataFrameBuilder = None,
                      algorithm_settings: AfeSupervisedAlgorithmSettings = None) -> Optional[IDataPartition]:
        """Get partition for frame builder data"""
        partition = DataPartition(frame_builder.frame)
        partition.partition(algorithm_settings.training_percentage)
        return partition

    def get_selected_cols(self, num_threads: int,
                          partition: IDataPartition = None,
                          algorithm_settings: AfeSupervisedAlgorithmSettings = None,
                          frame_builder: DataFrameBuilder = None,
                          frame_with_all_columns: DictDataFrame = None,
                          is_final=False) -> List[str]:
        """Selects best afe columns by modelling"""
        target_descriptor = self._settings.data_source_settings.target_descriptor

        categorical_features = self.__get_categorical_features(frame_builder, frame_with_all_columns.get_column_names())

        model = MultiTargetModellingHelper.__build_model(num_threads,
                                                         frame_builder.target_array,
                                                         target_descriptor, partition,
                                                         frame_with_all_columns,
                                                         algorithm_settings, categorical_features, is_final)
        selected_cols = []
        if model is not None and not model.empty:
            selected_cols.extend(model["variable"])

        return selected_cols

    @staticmethod
    def __get_categorical_features(frame_builder: DataFrameBuilder, column_names: List[str] = None) \
            -> List[str]:
        categorical_features = []
        for afe_column_name in column_names:
            afe_column = frame_builder.name_to_column[afe_column_name]
            if AfeOperator.Mode.name == afe_column.operator.name:
                categorical_features.append(afe_column_name)
        return categorical_features

    # pylint: disable=too-many-arguments
    @staticmethod
    def __build_model(num_of_threads: int,
                      target_array: np.array,
                      target_descriptor: TargetDescriptor,
                      partition: IDataPartition,
                      frame_with_all_columns: DictDataFrame,
                      algorithm_settings: AfeSupervisedAlgorithmSettings,
                      categorical_feature_list: List[str],
                      is_final=False):
        if is_final:
            model_settings: ModelSettings = algorithm_settings.final_model_settings
        else:
            model_settings: ModelSettings = algorithm_settings.model_settings

        y_all = target_array
        train_cols = frame_with_all_columns.get_column_names()
        if len(train_cols) == 0:
            raise KnownException("There are no frame columns to build model!")
        x_all = frame_with_all_columns.get_subset_as_pandas_df(columns=train_cols)

        for feature in categorical_feature_list:
            x_all[feature] = x_all[feature].astype("category")

        lgbm = MultiTargetModellingHelper.__get_lgbm_modeller(target_descriptor.target_column.target_column_type,
                                                              model_settings, num_of_threads,
                                                              categorical_feature_list)

        if partition.validation_indices is None:
            raise KnownException(
                "Validation set cannot be empty for lightgbm classifier. Please update training_percentage")
        with contextlib.redirect_stdout(None):
            lgbm.fit(x_all.iloc[partition.training_indices], y_all[partition.training_indices],
                     eval_set=[[x_all.iloc[partition.validation_indices], y_all[partition.validation_indices]]],
                     **model_settings.model_fit_params, verbose=0)

        imp_df_lgbm = pd.DataFrame(lgbm.feature_importances_, columns=['importance'], index=x_all.columns)
        imp_df_lgbm['imp_ratio'] = imp_df_lgbm['importance'] / imp_df_lgbm['importance'].sum()
        imp_df_lgbm.sort_values(by=['imp_ratio'], ascending=[False], inplace=True)
        imp_df_lgbm['cum_importance_perc'] = imp_df_lgbm['imp_ratio'].cumsum()
        if imp_df_lgbm['cum_importance_perc'].iloc[0] >= model_settings.reduction_coverage:
            imp_df_lgbm = imp_df_lgbm.iloc[[0]]
        else:
            imp_df_lgbm = imp_df_lgbm[imp_df_lgbm['cum_importance_perc'] <= model_settings.reduction_coverage]
        imp_df_lgbm = imp_df_lgbm.reset_index()[['index', 'importance']].rename(columns={'index': 'variable'})
        return imp_df_lgbm

    def get_final_columns_metrics(self, num_threads: int, frame_builder: DataFrameBuilder,
                                  frame_with_all_columns: DictDataFrame, reduced_columns: List[str],
                                  algorithm_settings: AfeSupervisedAlgorithmSettings) -> dict:
        """Returns modelling metrics as a dictionary"""
        y_all = frame_builder.target_array

        model_settings = algorithm_settings.final_model_settings
        target_descriptor = self._settings.data_source_settings.target_descriptor

        categorical_features = self.__get_categorical_features(frame_builder, reduced_columns)

        x_all = frame_with_all_columns.get_subset_as_pandas_df(columns=reduced_columns)

        for feature in categorical_features:
            x_all[feature] = x_all[feature].astype("category")

        train_indices, validation_indices, test_indices = self.__get_indices_for_final_col_metrics_model(
            len(x_all),
            algorithm_settings.training_percentage
        )
        lgbm = self.__get_lgbm_modeller(target_descriptor.target_column.target_column_type, model_settings,
                                        num_threads, categorical_features)
        with contextlib.redirect_stdout(None):
            lgbm.fit(x_all.iloc[train_indices], y_all[train_indices],
                     eval_set=[[x_all.iloc[validation_indices], y_all[validation_indices]]],
                     **model_settings.model_fit_params, verbose=0)

        y_test = y_all[test_indices]
        fpr, tpr, auc_val = {}, {}, {}
        target_col = target_descriptor.target_column
        if target_col.target_column_type == AfeTargetColumnType.Binary:
            y_pred = lgbm.predict_proba(x_all.iloc[test_indices])[:, 1]
            fpr["all"], tpr["all"], _ = roc_curve(y_test, y_pred,
                                                  pos_label=target_col.binary_target_info.positive_category)

            auc_val["all"] = auc(fpr["all"], tpr["all"])
        elif target_descriptor.target_column.target_column_type == AfeTargetColumnType.MultiClass:
            classes = lgbm.classes_
            y_pred = lgbm.predict_proba(x_all.iloc[test_indices])
            y_test_one_hot = np.ndarray((len(test_indices), len(classes)))
            for i, cls in enumerate(classes):
                y_test_one_hot[:, i] = np.array(y_test == cls).astype(int)
                fpr[cls], tpr[cls], _ = roc_curve(y_test_one_hot[:, i], y_pred[:, i])
                auc_val[cls] = auc(fpr[cls], tpr[cls])
            fpr["micro"], tpr["micro"], _ = roc_curve(y_test_one_hot.ravel(), y_pred.ravel())
            auc_val["micro"] = auc(fpr["micro"], tpr["micro"])
            all_fpr = np.unique(np.concatenate([fpr[cls] for cls in classes]))
            mean_tpr = np.zeros_like(all_fpr)
            for cls in classes:
                mean_tpr += np.interp(all_fpr, fpr[cls], tpr[cls])
            mean_tpr /= len(classes)
            fpr["macro"] = all_fpr
            tpr["macro"] = mean_tpr
            auc_val["macro"] = auc(fpr["macro"], tpr["macro"])

        feature_importance = pd.DataFrame(sorted(zip(lgbm.feature_importances_, x_all.columns), reverse=True),
                                          columns=['Value', 'Feature'])

        return {"fpr": fpr, "tpr": tpr, "auc": auc_val, "feature_importances": feature_importance}

    @staticmethod
    def __get_indices_for_final_col_metrics_model(frame_length: int, training_percentage: float):
        system_random = random.SystemRandom()
        if training_percentage >= 1.0:
            training_ratio = 0.6
            validation_ratio = 0.2
        else:
            training_ratio = training_percentage ** 2
            validation_ratio = training_percentage - training_ratio
        t_list = []
        v_list = []
        test_list = []
        for i in range(frame_length):
            rand_num = system_random.uniform(0, 1)
            if rand_num <= training_ratio:
                t_list.append(i)
            elif rand_num <= training_ratio + validation_ratio:
                v_list.append(i)
            else:
                test_list.append(i)
        training_indices = t_list
        validation_indices = v_list
        test_indices = test_list

        return training_indices, validation_indices, test_indices

    def control_target_record_files(self, multi_target_entity_container_service: MultiTargetEntityContainerService):
        """Controls min_data_in_leaf an sample_size values and logs a warning if necessary"""
        record_counts = []
        for record in multi_target_entity_container_service.container.records_per_file.values():
            record_counts.append(record.actual_record_count)
        min_sample_size = min(record_counts)

        final_model_settings: ModelSettings = self._settings.algorithm_settings.final_model_settings

        model_settings: ModelSettings = self._settings.algorithm_settings.model_settings
        min_data_in_leaf_and_sample_size_control_ratio = \
            self._settings.algorithm_settings.min_data_in_leaf_and_sample_size_control_ratio

        if (final_model_settings.model_params["min_data_in_leaf"] >
                min_sample_size * min_data_in_leaf_and_sample_size_control_ratio or
                model_settings.model_params["min_data_in_leaf"] >
                min_sample_size * min_data_in_leaf_and_sample_size_control_ratio):
            LogHelper.warning("Entered min_data_in_leaf is too large for the sample size "
                              "so model will not be established.")

    @staticmethod
    def __get_lgbm_modeller(target_column_type: AfeTargetColumnType, model_settings: ModelSettings,
                            num_of_threads: int, categorical_feature_list: List[str]):
        n_jobs = num_of_threads
        if n_jobs is None or n_jobs == 0:
            n_jobs = -1
        if target_column_type == AfeTargetColumnType.Binary:
            model_settings.model_fit_params.setdefault('eval_metric', 'auc')
            model_settings.model_params.setdefault('objective', 'binary')
            lgbm = LGBMClassifier(n_jobs=n_jobs, categorical_feature=categorical_feature_list,
                                  **model_settings.model_params)
        elif target_column_type == AfeTargetColumnType.Scalar:
            model_settings.model_fit_params.setdefault('eval_metric', 'mape')
            lgbm = LGBMRegressor(n_jobs=n_jobs, categorical_feature=categorical_feature_list,
                                 **model_settings.model_params)
        elif target_column_type == AfeTargetColumnType.MultiClass:
            model_settings.model_fit_params.setdefault('eval_metric', 'multi_logloss')
            model_settings.model_params.setdefault('objective', 'multiclass')
            lgbm = LGBMClassifier(n_jobs=n_jobs, categorical_feature=categorical_feature_list,
                                  **model_settings.model_params)
        else:
            raise KnownException("Unknown target type :" + target_column_type)
        return lgbm
