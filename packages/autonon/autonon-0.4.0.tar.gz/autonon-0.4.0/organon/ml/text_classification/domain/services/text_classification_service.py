"""Includes TextClassificationService class for Text Classification"""
import itertools
import os
from typing import Union, Tuple, Optional

import numpy as np
import pandas as pd
import tensorflow as tf
from datasets import Dataset, load_dataset
from sklearn.model_selection import train_test_split

from organon.fl.logging.helpers.log_helper import LogHelper
from organon.ml.text_classification.domain.enums.model_run_type import ModelRunType
from organon.ml.text_classification.domain.enums.classification_languages import ClassificationLanguages
from organon.ml.text_classification.domain.enums.selection_metrics import SelectionMetrics
from organon.ml.text_classification.domain.objects.text_classification_settings import TextClassificationSettings
from organon.ml.text_classification.domain.enums.model_checkpoints import ModelCheckpoints
from organon.ml.text_classification.domain.objects.tokenizer_settings import TokenizerSettings

# pylint: disable=import-outside-toplevel


class TextClassificationService:
    """Text Classification Domain Service"""

    BINARY_CHECKPOINTS = [ModelCheckpoints.BERT_BASE_TR_128, ModelCheckpoints.BERT_BASE_TR_SENTIMENT]
    TURKISH_CHECKPOINTS = [ModelCheckpoints.BERT_BASE_MLINGUAL, ModelCheckpoints.BERT_BASE_TR_128,
                           ModelCheckpoints.BERT_BASE_TR_SENTIMENT]
    ENGLISH_CHECKPOINTS = [ModelCheckpoints.BERT_BASE_MLINGUAL, ModelCheckpoints.ROBERTA_BASE,
                           ModelCheckpoints.BERT_BASE, ModelCheckpoints.DISTILBERT_BASE]
    val_loss_key = 'Loss'
    accuracy_key = 'Accuracy'
    roc_auc_score_key = 'Roc-Auc Score'
    f1_score_key = 'F1-Score'

    def __init__(self, settings: TextClassificationSettings):
        from transformers import logging as transformers_log
        tf.get_logger().setLevel('ERROR')
        transformers_log.set_verbosity_error()
        if tf.config.list_physical_devices('GPU'):
            LogHelper.warning("GPU is available")
        else:
            LogHelper.warning("GPU is NOT available")

        self._settings = settings
        self.is_trained = False
        self.model = None
        self.grid_search_params_dict: dict = None
        self.best_params_dict: dict = None
        self.metrics: dict = None
        self._num_labels: int = None
        self._tokenizer = None
        self._predictions: np.ndarray = None
        self._label_column = "label"

    def predict(self, test_data: Union[str, Tuple[str, Optional[str]], pd.DataFrame]):
        """predict sample from trained model"""
        x_test = self._load_test_data(test_data)
        self._check_trained()
        predictions = self._calculate_preds(x_test)
        class_predictions = np.argmax(predictions, axis=1)
        return class_predictions

    def predict_proba(self, test_data: Union[str, Tuple[str, Optional[str]], pd.DataFrame]):
        """predict probability values for test texts"""
        from sklearn.metrics import roc_auc_score
        from scipy.special import softmax

        x_test = self._load_test_data(test_data)
        self._check_trained()
        predictions = self._calculate_preds(x_test)
        predictions_softmax = softmax(predictions, axis=1)
        if self._num_labels > 2:
            roc_scr = roc_auc_score(x_test[self._label_column], predictions_softmax, multi_class='ovr')
        else:
            roc_scr = roc_auc_score(x_test[self._label_column], predictions_softmax[:, 1],
                                    multi_class='ovr')

        return predictions_softmax, roc_scr

    def fit(self, data: Union[str, Tuple[str, Optional[str]], pd.DataFrame],
            validation_data: Union[str, pd.DataFrame] = None, validation_data_ratio: float = 0.2,
            random_seed: int = None, sample_weights_flag: bool = True):
        """fit the Text Classification Model"""
        train_data, val_data = self._load_data(data, validation_data, validation_data_ratio, random_seed)
        self._num_labels = len(np.unique(train_data[self._label_column]))

        if self._settings.mdl_run_type == ModelRunType.EFFICIENT:
            self._check_language_checkpoint(self._settings.checkpoint)
            TextClassificationService._check_cls_type(self._settings.checkpoint, self._num_labels)
            model_checkpoint = TextClassificationService._get_checkpoint(self._settings.checkpoint)

            tokenized_x_train, tf_train_set, tf_validation_set, train_class_weights = \
                self._training_preprocess(train_data, val_data, model_checkpoint,
                                          self._settings.mdl_param_settings.batch_size)

            optimizer, callback = \
                TextClassificationService._load_optimizer(tokenized_x_train,
                                                          self._settings.mdl_param_settings.batch_size,
                                                          self._settings.mdl_param_settings.epochs,
                                                          self._settings.opt_settings.learning_rate,
                                                          self._settings.opt_settings.early_stopping,
                                                          self._settings.opt_settings.early_stopping_min_delta)

            model, metrics = self._model_run(val_data=val_data, model_checkpoint=model_checkpoint,
                                             tf_train_set=tf_train_set, tf_validation_set=tf_validation_set,
                                             num_epochs=self._settings.mdl_param_settings.epochs,
                                             optimizer=optimizer, callback=callback,
                                             steps_per_epoch=self._settings.opt_settings.steps_per_epoch,
                                             train_class_weights=train_class_weights,
                                             sample_weights_flag=sample_weights_flag)

            self.model = model
            self.is_trained = True
            self.metrics = metrics

        elif self._settings.mdl_run_type == ModelRunType.HIGH_PERFORMANCE:

            if self._settings.grid_src_settings is not None:
                for checkpoint in self._settings.grid_src_settings.models:
                    self._check_language_checkpoint(checkpoint)

                best_model, best_metrics, best_params, params_dict = self._grid_search(train_data, val_data,
                                                                                       sample_weights_flag)
                self.model = best_model
                self.is_trained = True
                self.metrics = best_metrics
                self.grid_search_params_dict = params_dict
                self.best_params_dict = best_params
            else:
                raise ValueError("Grid Search Settings cannot be None.")
        else:
            raise ValueError("Model Run Type has not specified.")
    @staticmethod
    def load_csv_data(train_data_file: str, validation_data_file: str = None, validation_data_ratio: float = 0.2,
                      random_seed: int = None):
        """load text classification data and turn it to dataframe"""
        if os.path.exists(train_data_file):
            train_data = pd.read_csv(train_data_file)
            if os.path.exists(validation_data_file):
                validation_data = pd.read_csv(validation_data_file)
                return train_data, validation_data
            x_train, x_val = train_test_split(train_data, test_size=validation_data_ratio,
                                              random_state=random_seed)
            return x_train, x_val
        raise FileNotFoundError("csv path can not be located.")

    @staticmethod
    def load_dataframe(train_data: pd.DataFrame, validation_data: pd.DataFrame = None,
                       validation_data_ratio: float = 0.2, random_seed: int = None):
        """load text classification data as dataframe"""
        if validation_data is not None:
            if train_data.empty and validation_data.empty:
                raise ValueError("DataFrames can not be empty")
            return train_data, validation_data
        x_train, x_val = train_test_split(train_data, test_size=validation_data_ratio,
                                          random_state=random_seed)
        return x_train, x_val

    @staticmethod
    def load_hf_data(dataset_name: str = None, subset: str = None, validation_data_ratio: float = 0.2,
                     random_seed: int = None):
        """using load_dataset method, create Hugging Face dataframes"""
        if dataset_name is None:
            raise ValueError("dataset name can not be None")
        if subset is not None:
            hf_dataset = load_dataset(dataset_name, subset)
            if 'validation' in hf_dataset.keys():
                train_data = pd.DataFrame(hf_dataset['train'])
                val_data = pd.DataFrame(hf_dataset['validation'])
            else:
                train_data, val_data = train_test_split(pd.DataFrame(hf_dataset['train']),
                                                        test_size=validation_data_ratio,
                                                        random_state=random_seed)
        else:
            hf_dataset = load_dataset(dataset_name)
            if 'validation' in hf_dataset.keys():
                train_data = pd.DataFrame(hf_dataset['train'])
                val_data = pd.DataFrame(hf_dataset['validation'])
            else:
                train_data, val_data = train_test_split(pd.DataFrame(hf_dataset['train']),
                                                        test_size=validation_data_ratio,
                                                        random_state=random_seed)
        del hf_dataset
        return train_data, val_data

    def _load_data(self, data: Union[str, Tuple[str, Optional[str]], pd.DataFrame],
                   validation_data: Union[str, pd.DataFrame] = None, validation_data_ratio: float = 0.2,
                   random_seed: int = None):
        """load and check data properties"""
        inplace_flag = False
        if isinstance(data, str):
            if self._settings.text_column is None:
                raise ValueError("CSV text column name must be specified")
            if self._settings.target_column is None:
                raise ValueError("CSV target column name must be specified")
            train_data, val_data = TextClassificationService.load_csv_data(data, validation_data, validation_data_ratio,
                                                                           random_seed)
            inplace_flag = True
        elif isinstance(data, Tuple):
            if self._settings.text_column is None:
                raise ValueError("HF Data text column name must be specified")
            if self._settings.target_column is None:
                raise ValueError("HF Data target column name must be specified")
            train_data, val_data = TextClassificationService.load_hf_data(data[0], data[1], validation_data_ratio,
                                                                          random_seed)
            inplace_flag = True
        elif isinstance(data, pd.DataFrame):
            if self._settings.text_column is None:
                raise ValueError("DataFrame text column name must be specified")
            if self._settings.target_column is None:
                raise ValueError("DataFrame target column name must be specified")
            train_data, val_data = TextClassificationService.load_dataframe(data, validation_data,
                                                                            validation_data_ratio, random_seed)
        else:
            raise TypeError("Either pass CSV file path, pandas Dataframe or HF dataset keyword to train the model.")
        train_data = TextClassificationService._check_target_column_name(train_data, self._settings.target_column,
                                                                         inplace_flag)
        val_data = TextClassificationService._check_target_column_name(val_data, self._settings.target_column,
                                                                       inplace_flag)

        return train_data, val_data

    def _load_test_data(self, test_data: Union[str, Tuple[str, Optional[str]], pd.DataFrame]):
        """loads test data for predict and predict_proba methods"""
        inplace_flag = False
        if isinstance(test_data, str):
            test_data = pd.read_csv(test_data)
            inplace_flag = True
        elif isinstance(test_data, Tuple):
            test_data = pd.DataFrame(load_dataset(test_data[0], test_data[1], split="test"))
            inplace_flag = True
        elif isinstance(test_data, pd.DataFrame):
            pass
        else:
            raise TypeError("Either pass CSV file path, pandas Dataframe or HF dataset keyword to make predictions.")
        test_data = TextClassificationService._check_target_column_name(test_data, self._settings.target_column,
                                                                        inplace_flag)
        return test_data

    def _check_trained(self):
        """check if model trained, this method will constrain the usage of predict and predict_proba before training"""
        if not self.is_trained:
            raise Exception("Trainer is not trained yet.")

    def _calculate_preds(self, test_data: pd.DataFrame):
        """calculate prediction probabilities with tokenized test set"""
        tokenized_test_set = TextClassificationService._tokenize_data_words \
            (test_data, self._tokenizer,
             self._settings.text_column,
             self._settings.tokenizer_settings,
             False,
             self._settings.mdl_param_settings.batch_size)
        predictions = self.model.predict(tokenized_test_set)['logits']
        return predictions

    def _grid_search(self, train_data: pd.DataFrame, val_data: pd.DataFrame, sample_weights_flag: bool):
        """grid search algorithm for high performance Text Classification"""
        best_model = None
        best_params = []
        grid_search_lists = [
            self._settings.grid_src_settings.models, self._settings.grid_src_settings.batch_sizes,
            self._settings.grid_src_settings.epochs, self._settings.grid_src_settings.learning_rates,
            self._settings.grid_src_settings.early_stopping_patiences,
            self._settings.grid_src_settings.early_stopping_min_deltas
        ]
        best_score = float('-inf')
        best_loss = float('inf')
        params_dict = {}
        best_metrics = {}
        step_id = 1
        for run_step in itertools.product(*grid_search_lists):
            LogHelper.warning(f"Grid Search is running for {run_step[0].name}")
            params_info = "Grid Search Parameters: \n" + f"Checkpoint: {run_step[0].name}\n" + \
                           f"Batch Size: {run_step[1]}\n" + f"Epoch: {run_step[2]}\n" +\
                           f"Learning Rate: {run_step[3]}\n" +\
                           f"Early Stopping Patience: {run_step[4]}\n" +\
                           f"Early Stopping Min Delta: {run_step[5]}\n"
            LogHelper.warning(params_info)
            model_checkpoint = TextClassificationService._get_checkpoint(run_step[0])
            TextClassificationService._check_cls_type(run_step[0], self._num_labels)
            tokenized_x_train, tf_train_set, tf_validation_set, train_class_weights = self._training_preprocess(
                train_data, val_data, model_checkpoint, run_step[1])
            optimizer, callback = TextClassificationService._load_optimizer(tokenized_x_train, batch_size=run_step[1],
                                                                            num_epochs=run_step[2],
                                                                            learning_rate=run_step[3],
                                                                            early_stopping_patience=run_step[4],
                                                                            early_stopping_min_delta=run_step[5]
                                                                            )
            model, selection_metrics = self._model_run(val_data=val_data, model_checkpoint=model_checkpoint,
                                                       tf_train_set=tf_train_set, tf_validation_set=tf_validation_set,
                                                       num_epochs=run_step[2], optimizer=optimizer, callback=callback,
                                                       steps_per_epoch=self._settings.opt_settings.steps_per_epoch,
                                                       train_class_weights=train_class_weights,
                                                       sample_weights_flag=sample_weights_flag)
            LogHelper.warning(
                f"{TextClassificationService.accuracy_key}: {selection_metrics[TextClassificationService.accuracy_key]}"
               f"{TextClassificationService.val_loss_key}: {selection_metrics[TextClassificationService.val_loss_key]}")
            params = {'Checkpoint': run_step[0].name, 'Batch Size': run_step[1],
                      'Epoch': run_step[2], 'Learning Rate': run_step[3],
                      'Early Stopping Patience': run_step[4],
                      'Early Stopping Min Delta': run_step[5],
                      TextClassificationService.accuracy_key: selection_metrics[TextClassificationService.accuracy_key],
                      TextClassificationService.val_loss_key: selection_metrics[TextClassificationService.val_loss_key],
                      TextClassificationService.roc_auc_score_key: selection_metrics[
                          TextClassificationService.roc_auc_score_key],
                      TextClassificationService.f1_score_key: selection_metrics[TextClassificationService.f1_score_key]}
            params_dict[f"Step {step_id}"] = params
            best_metrics, best_model, best_params, best_loss, best_score = self._determine_best_model(model, run_step,
                                                                                                      best_metrics,
                                                                                                      best_model,
                                                                                                      best_params,
                                                                                                      best_loss,
                                                                                                      best_score,
                                                                                                      selection_metrics)
            step_id += 1
        best_params_dict = {'Checkpoint': best_params[0].name, 'Batch Size': best_params[1],
                            'Epoch': best_params[2], 'Learning Rate': best_params[3],
                            'Early Stopping Patience': best_params[4],
                            'Early Stopping Min Delta': best_params[5]}
        return best_model, best_metrics, best_params_dict, params_dict

    def _determine_best_model(self, model, run_step, best_metrics, best_model, best_params, best_loss: float,
                              best_score: float, selection_metrics):
        """determination logic for given metrics"""
        # pylint: disable=too-many-arguments
        if self._settings.grid_src_settings.model_selection_metric == SelectionMetrics.VAL_LOSS:
            if best_loss > selection_metrics[TextClassificationService.val_loss_key]:
                best_loss = selection_metrics[TextClassificationService.val_loss_key]
                best_score = selection_metrics[TextClassificationService.accuracy_key]
                best_model = model
                best_params = run_step
                best_metrics = {TextClassificationService.val_loss_key: best_loss,
                                TextClassificationService.accuracy_key: best_score}
        elif self._settings.grid_src_settings.model_selection_metric == SelectionMetrics.ACC_SCORE:
            if best_score < selection_metrics[TextClassificationService.accuracy_key]:
                best_loss = selection_metrics[TextClassificationService.val_loss_key]
                best_score = selection_metrics[TextClassificationService.accuracy_key]
                best_model = model
                best_params = run_step
                best_metrics = {TextClassificationService.val_loss_key: best_loss,
                                TextClassificationService.accuracy_key: best_score}
        elif self._settings.grid_src_settings.model_selection_metric == SelectionMetrics.ROC_AUC:
            if best_score < selection_metrics[TextClassificationService.roc_auc_score_key]:
                best_loss = selection_metrics[TextClassificationService.val_loss_key]
                best_score = selection_metrics[TextClassificationService.roc_auc_score_key]
                best_model = model
                best_params = run_step
                best_metrics = {TextClassificationService.val_loss_key: best_loss,
                                TextClassificationService.roc_auc_score_key: best_score}
        elif self._settings.grid_src_settings.model_selection_metric == SelectionMetrics.F1_SCORE:
            if best_score < selection_metrics[TextClassificationService.f1_score_key]:
                best_loss = selection_metrics[TextClassificationService.val_loss_key]
                best_score = selection_metrics[TextClassificationService.f1_score_key]
                best_model = model
                best_params = run_step
                best_metrics = {TextClassificationService.val_loss_key: best_loss,
                                TextClassificationService.f1_score_key: best_score}
        else:
            LogHelper.error("Can not determine the best model with given metric.")
        return best_metrics, best_model, best_params, best_loss, best_score

    def _model_run(self, val_data, model_checkpoint: str, tf_train_set, tf_validation_set,
                   num_epochs: int, optimizer, callback, steps_per_epoch: int, train_class_weights,
                   sample_weights_flag: bool):
        # pylint: disable=too-many-arguments
        """runs the specified model"""
        from transformers import TFAutoModelForSequenceClassification
        from scipy.special import softmax

        model = TFAutoModelForSequenceClassification.from_pretrained(model_checkpoint,
                                                                     num_labels=self._num_labels, from_pt=True)

        def add_sample_weights(data):
            # The weights for each class, with the constraint that:
            #     sum(class_weights) == 1.0
            class_weights = tf.constant(list(train_class_weights.values()))
            class_weights = class_weights / tf.reduce_sum(class_weights)

            # Create an image of `sample_weights` by using the label at each pixel as an
            # index into the `class weights` .
            sample_weights = tf.gather(class_weights, indices=tf.cast(data['labels'], tf.int32), axis=0)

            return data, sample_weights

        model.compile(optimizer=optimizer)

        if sample_weights_flag:
            model.fit(x=tf_train_set.map(add_sample_weights),
                      validation_data=tf_validation_set,
                      epochs=num_epochs, callbacks=[callback], steps_per_epoch=steps_per_epoch)
        else:
            model.fit(x=tf_train_set,
                      validation_data=tf_validation_set,
                      epochs=num_epochs, callbacks=[callback], steps_per_epoch=steps_per_epoch)

        loss = model.evaluate(tf_validation_set)
        predictions = model.predict(tf_validation_set)['logits']
        val_predictions_softmax = softmax(predictions, axis=1)
        val_class_predictions = np.argmax(predictions, axis=1)
        val_roc, val_acc, val_f1 = self._calculate_metrics_with_val_data(val_data, val_predictions_softmax,
                                                                         val_class_predictions)
        selection_metrics = {TextClassificationService.val_loss_key: loss,
                             TextClassificationService.roc_auc_score_key: val_roc,
                             TextClassificationService.accuracy_key: val_acc,
                             TextClassificationService.f1_score_key: val_f1}

        return model, selection_metrics

    def _calculate_metrics_with_val_data(self, val_data: pd.DataFrame, predictions_softmax, val_class_predictions):
        """calculate metrics for model evaluation"""
        from sklearn.metrics import roc_auc_score, accuracy_score, f1_score
        if self._num_labels > 2:
            val_roc_auc = roc_auc_score(val_data[self._label_column], predictions_softmax, average="weighted",
                                        multi_class='ovr')
            val_acc = accuracy_score(val_data[self._label_column], val_class_predictions)
            val_f1 = f1_score(val_data[self._label_column], val_class_predictions, average='weighted')
        else:
            val_roc_auc = roc_auc_score(val_data[self._label_column], predictions_softmax[:, 1])
            val_acc = accuracy_score(val_data[self._label_column], val_class_predictions)
            val_f1 = f1_score(val_data[self._label_column], val_class_predictions)

        return val_roc_auc, val_acc, val_f1

    def _training_preprocess(self, train_data: pd.DataFrame, val_data: pd.DataFrame, model_checkpoint: str,
                             batch_size: int):
        """tokenize data for model tranining"""
        from transformers import AutoTokenizer
        from sklearn.utils import class_weight
        self._tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

        tf_train_set, tokenized_x_train = \
            TextClassificationService._tokenize_data_words(train_data, self._tokenizer,
                                                           self._settings.text_column,
                                                           self._settings.tokenizer_settings,
                                                           shuffle=True,
                                                           batch_size=batch_size)

        tf_validation_set = TextClassificationService._tokenize_data_words(val_data, self._tokenizer,
                                                                           self._settings.text_column,
                                                                           self._settings.tokenizer_settings,
                                                                           shuffle=False, batch_size=batch_size)

        class_weights = class_weight.compute_class_weight(class_weight='balanced',
                                                          classes=np.unique(train_data.label),
                                                          y=train_data.label)

        train_class_weights = dict(enumerate(class_weights))
        return tokenized_x_train, tf_train_set, tf_validation_set, train_class_weights

    @staticmethod
    def _load_optimizer(tokenized_x_train, batch_size: int, num_epochs: int, learning_rate: float,
                        early_stopping_patience: int, early_stopping_min_delta: float):
        """using create optimizer method, make the optimizer ready for training"""
        from keras.callbacks import EarlyStopping
        optimizer = TextClassificationService._create_optimizer(tokenized_x_train, batch_size, num_epochs,
                                                                learning_rate)

        callback = [
            EarlyStopping(patience=early_stopping_patience,
                          min_delta=early_stopping_min_delta, monitor='val_loss')
        ]
        return optimizer, callback

    @staticmethod
    def _tokenize_data_words(data: pd.DataFrame, tokenizer, text_column: str,
                             tokenizer_settings: TokenizerSettings, shuffle: bool, batch_size: int):
        """general purpose dataset tokenization method"""
        from transformers import DataCollatorWithPadding

        def tokenize_function(text_data: pd.DataFrame):
            """tokenize all the text data and return it with the help of the map method"""
            return tokenizer(text_data[text_column], padding=tokenizer_settings.padding,
                             truncation=tokenizer_settings.truncation, max_length=tokenizer_settings.max_length)

        data_d = Dataset.from_pandas(data)
        tokenized_data = data_d.map(tokenize_function, batched=True)
        del data_d
        data_collator = DataCollatorWithPadding(tokenizer=tokenizer, return_tensors='tf')
        data_set = tokenized_data.to_tf_dataset(
            columns=["attention_mask", "input_ids", "label"],
            shuffle=shuffle,  # True for train data, False for both validation and test data
            batch_size=batch_size,
            collate_fn=data_collator
        )
        if shuffle:
            return data_set, tokenized_data
        return data_set

    @staticmethod
    def _get_checkpoint(checkpoint_enum: ModelCheckpoints):
        if checkpoint_enum == ModelCheckpoints.BERT_BASE:
            return "bert-base-cased"
        if checkpoint_enum == ModelCheckpoints.DISTILBERT_BASE:
            return "distilbert-base-uncased"
        if checkpoint_enum == ModelCheckpoints.ROBERTA_BASE:
            return "roberta-base"
        if checkpoint_enum == ModelCheckpoints.BERT_BASE_TR_128:
            return "dbmdz/bert-base-turkish-128k-cased"
        if checkpoint_enum == ModelCheckpoints.BERT_BASE_MLINGUAL:
            return "bert-base-multilingual-cased"
        if checkpoint_enum == ModelCheckpoints.BERT_BASE_TR_SENTIMENT:
            return "savasy/bert-base-turkish-sentiment-cased"

        raise ValueError("Specified checkpoint can not be supported.")

    @staticmethod
    def _create_optimizer(tokenized_x_train, batch_size: int, epochs: int, learning_rate: float):
        """method for model optimizer"""
        from transformers import create_optimizer
        batches_per_epoch = len(tokenized_x_train) // batch_size
        total_train_steps = int(batches_per_epoch * epochs)
        # pylint: disable=assignment-from-no-return
        optimizer, _ = create_optimizer(init_lr=learning_rate, num_warmup_steps=0,
                                        num_train_steps=total_train_steps)

        return optimizer

    @staticmethod
    def _check_cls_type(checkpoint: ModelCheckpoints, num_labels: int):
        """Check if inappropriate checkpoint usage occurs"""
        if num_labels > 2:
            if checkpoint in TextClassificationService.BINARY_CHECKPOINTS:
                raise TypeError("This type of checkpoint can't be used in Multiclass Classification")

    def _check_language_checkpoint(self, checkpoint: ModelCheckpoints):
        """check if selected checkpoint is appropriate for data language"""
        if self._settings.language == ClassificationLanguages.TURKISH:
            if checkpoint not in TextClassificationService.TURKISH_CHECKPOINTS:
                raise ValueError(f"Checkpoint named {checkpoint} is non-Turkish")
        elif self._settings.language == ClassificationLanguages.ENGLISH:
            if checkpoint not in TextClassificationService.ENGLISH_CHECKPOINTS:
                raise ValueError(f"Checkpoint named {checkpoint} is non-English")
        else:
            raise ValueError("Given language cannot be supported.")

    @staticmethod
    def _check_target_column_name(data: pd.DataFrame, target_column: str, inplace_flag: bool):
        """check if target column name set to 'label' if not, set it as 'label'"""
        if target_column != "label":
            if inplace_flag:
                data.rename(columns={target_column: 'label'}, inplace=True)
            else:
                data = data.rename(columns={target_column: 'label'})
        return data
