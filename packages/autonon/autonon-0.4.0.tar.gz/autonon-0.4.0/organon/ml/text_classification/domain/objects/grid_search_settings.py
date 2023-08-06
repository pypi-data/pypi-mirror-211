"""settings class for Grid Search Text Classification Models"""
from typing import List

from organon.ml.text_classification.domain.enums.model_checkpoints import ModelCheckpoints
from organon.ml.text_classification.domain.enums.selection_metrics import SelectionMetrics


class GridSearchSettings:
    """Class for grid search parameters"""

    def __init__(self, models: List[ModelCheckpoints] = None, batch_sizes: List[int] = None, epochs: List[int] = None,
                 learning_rates: List[float] = None, early_stopping_patiences: List[int] = None,
                 early_stopping_min_deltas: List[float] = None,
                 model_selection_metric: SelectionMetrics = SelectionMetrics.VAL_LOSS):
        # pylint: disable=too-many-arguments
        self.models = models if models is not None else [ModelCheckpoints.BERT_BASE,
                                                         ModelCheckpoints.BERT_BASE_MLINGUAL]
        self.batch_sizes = batch_sizes if batch_sizes is not None else [8]
        self.epochs = epochs if epochs is not None else [2]
        self.learning_rates = learning_rates if learning_rates is not None else [1e-5]
        self.early_stopping_patiences = early_stopping_patiences if early_stopping_patiences is not None else [2]
        self.early_stopping_min_deltas = early_stopping_min_deltas if early_stopping_min_deltas is not None else [1e-3]
        self.model_selection_metric = model_selection_metric
