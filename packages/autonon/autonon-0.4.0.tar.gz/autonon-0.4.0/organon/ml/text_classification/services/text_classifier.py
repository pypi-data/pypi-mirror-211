"""Includes TextClassifier class"""
from typing import List, Tuple, Union, Optional

import pandas as pd

from organon.fl.core.helpers import list_helper
from organon.ml.common.helpers.user_input_service_helper import get_enum
from organon.ml.text_classification.domain.enums.classification_languages import ClassificationLanguages
from organon.ml.text_classification.domain.enums.model_checkpoints import ModelCheckpoints
from organon.ml.text_classification.domain.enums.model_run_type import ModelRunType
from organon.ml.text_classification.domain.enums.selection_metrics import SelectionMetrics
from organon.ml.text_classification.domain.objects.grid_search_settings import GridSearchSettings
from organon.ml.text_classification.domain.objects.model_parameter_settings import ModelParameterSettings
from organon.ml.text_classification.domain.objects.optimizer_settings import OptimizerSettings
from organon.ml.text_classification.domain.objects.text_classification_settings import TextClassificationSettings
from organon.ml.text_classification.domain.objects.tokenizer_settings import TokenizerSettings
from organon.ml.text_classification.domain.services.text_classification_service import TextClassificationService


class TextClassifier:
    """Text Classification UI class"""

    def __init__(self, mdl_run_type: str, checkpoint: str = None, text_column_name: str = None,
                 target_column_name: str = None,
                 language: str = ClassificationLanguages.ENGLISH.name):
        # pylint: disable=too-many-arguments
        model_run_type = get_enum(mdl_run_type.upper(), ModelRunType)
        if checkpoint is not None:
            model_checkpoint = get_enum(checkpoint.upper(), ModelCheckpoints)
        else:
            model_checkpoint = None
        model_language = get_enum(language.upper(), ClassificationLanguages)
        self._settings = TextClassificationSettings(language=model_language,
                                                    text_column=text_column_name,
                                                    target_column=target_column_name,
                                                    mdl_run_type=model_run_type,
                                                    checkpoint=model_checkpoint)
        self._mdl_parameter_settings: ModelParameterSettings = None
        self._optimizer_settings: OptimizerSettings = None
        self._grid_search_settings: GridSearchSettings = None
        self._tokenizer_settings: TokenizerSettings = None
        self._service: TextClassificationService = None
        self.grid_search_params_dict: dict = None
        self.best_model_dict: dict = None

    def fit(self, data: Union[str, Tuple[str, Optional[str]], pd.DataFrame],
            validation_data: Union[str, pd.DataFrame] = None, validation_data_ratio: float = 0.2,
            random_seed: int = None, add_sample_weights: bool = True):
        """fits the classifier"""
        self._set_full_settings()
        self._service = TextClassificationService(self._settings)
        self._service.fit(data, validation_data, validation_data_ratio, random_seed, add_sample_weights)
        self.grid_search_params_dict = self._service.grid_search_params_dict
        self.best_model_dict = self._service.best_params_dict

    def predict(self, test_data: Union[str, Tuple[str, Optional[str]], pd.DataFrame]):
        """prediction of given text example"""
        return self._service.predict(test_data)

    def predict_proba(self, test_data: Union[str, Tuple[str, Optional[str]], pd.DataFrame]):
        """prediction probabilities given text example"""
        return self._service.predict_proba(test_data)

    def set_optimizer_settings(self, learning_rate: float, early_stopping: int, steps_per_epoch: int,
                               early_stopping_min_delta: float):
        """Sets the model optimizer settings for model compilation"""
        self._optimizer_settings = OptimizerSettings(learning_rate, early_stopping, steps_per_epoch,
                                                     early_stopping_min_delta)

    def set_mdl_settings(self, batch_size: int = 20, epoch: int = 20):
        """Sets model parameter settings for model training"""
        self._mdl_parameter_settings = ModelParameterSettings(batch_size, epoch)

    def set_grid_search_settings(self, models: List[str], batch_sizes: List[int],
                                 epochs: List[int],
                                 learning_rates: List[float], early_stopping_patience: List[int],
                                 early_stopping_min_deltas: List[float],
                                 model_selection_metric: str = None):
        # pylint: disable=too-many-arguments
        """Sets grid search parameter settings for High performance classification"""
        model_checkpoints: List[ModelCheckpoints] = []
        if list_helper.is_null_or_empty(models):
            raise ValueError("Checkpoint List can not be empty")

        for checkpoint in models:
            model_checkpoints.append(get_enum(checkpoint.upper(), ModelCheckpoints))

        if model_selection_metric is not None:
            model_selection_metric = get_enum(model_selection_metric.upper(), SelectionMetrics)

        if list_helper.is_null_or_empty(batch_sizes):
            raise ValueError("Batch sizes List can not be empty")
        if list_helper.is_null_or_empty(epochs):
            raise ValueError("Epochs List can not be empty")
        if list_helper.is_null_or_empty(learning_rates):
            raise ValueError("Learning rates List can not be empty")
        if list_helper.is_null_or_empty(early_stopping_patience):
            raise ValueError("Stopping patience List can not be empty")
        if list_helper.is_null_or_empty(early_stopping_min_deltas):
            raise ValueError("Stopping min deltas List can not be empty")
        self._grid_search_settings = GridSearchSettings(model_checkpoints, batch_sizes, epochs, learning_rates,
                                                        early_stopping_patience, early_stopping_min_deltas,
                                                        model_selection_metric)

    def set_tokenizer_settings(self, padding: str, truncation: bool, max_length: int):
        """sets tokenizer settings for text tokenization"""
        self._tokenizer_settings = TokenizerSettings(padding, truncation, max_length)

    def _set_full_settings(self):
        """set all settings specifications of text classification"""
        if self._mdl_parameter_settings is not None:
            self._settings.mdl_param_settings = self._mdl_parameter_settings
        if self._grid_search_settings is not None:
            self._settings.grid_src_settings = self._grid_search_settings
        if self._optimizer_settings is not None:
            self._settings.opt_settings = self._optimizer_settings
        if self._tokenizer_settings is not None:
            self._settings.tokenizer_settings = self._tokenizer_settings
