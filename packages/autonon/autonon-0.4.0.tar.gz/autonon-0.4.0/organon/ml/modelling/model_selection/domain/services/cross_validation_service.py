"""Includes CrossValidationService class"""
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, PredefinedSplit, cross_val_score
from sklearn.preprocessing import KBinsDiscretizer

from organon.fl.mathematics.constants import DOUBLE_MIN

from organon.ml.modelling.algorithms.core.enums.modeller_type import ModellerType
from organon.ml.modelling.model_selection.domain.objects.cross_validation_output import CrossValidationOutput
from organon.ml.modelling.model_selection.settings.objects.cross_validation_settings import CrossValidationSettings

DEFAULT_CV_COUNT = 3
DEFAULT_BIN_COUNT = 10


class CrossValidationService:
    """Service for cross validation"""

    @classmethod
    def execute(cls, settings: CrossValidationSettings) -> CrossValidationOutput:
        """Runs multiple modellers with cross validation using same folds and report scores for every run"""
        modellers = settings.modellers
        modelling_type = modellers[0].modeller_type

        pds = cls.get_predefined_split(settings.train_data, settings.target_data, modelling_type, settings.cv_count,
                                       bin_count=settings.bin_count)

        output = CrossValidationOutput()
        output.fold_scores = []
        output.mean_scores = []
        best_score = DOUBLE_MIN
        best_modeller = None
        for modeller in modellers:  # modellers should be fitted in order
            res = cross_val_score(modeller, settings.train_data, settings.target_data, cv=pds)
            output.fold_scores.append(list(res))
            mean_score = np.mean(res)
            output.mean_scores.append(mean_score)
            if mean_score > best_score:
                best_score = mean_score
                best_modeller = modeller
        output.best_modeller = best_modeller
        if settings.return_test_fold:
            output.test_fold = pds.test_fold
        return output

    @classmethod
    def get_predefined_split(cls, train_data: pd.DataFrame, target_data: pd.Series, modeller_type: ModellerType,
                             cv_count: int = DEFAULT_CV_COUNT, bin_count: int = DEFAULT_BIN_COUNT):
        """Returns a PredefinedSplit instance for given train and target data"""
        if modeller_type == ModellerType.REGRESSOR:
            if bin_count is None:
                raise ValueError("bin_count should not be None for regression")
            target_data = cls._get_discretized(target_data, bin_count)
        return cls.get_predefined_split_for_stratified_target(train_data, target_data, cv_count)

    @classmethod
    def get_predefined_split_for_stratified_target(cls, train_data: pd.DataFrame, target_data: pd.Series,
                                                   cv_count: int = None):
        """Returns a PredefinedSplit instance for given train and target data.
        Should only be used for classification modelling."""
        fold = StratifiedKFold(n_splits=cv_count, shuffle=True)
        # StratifiedKFold uses target as the strata to generate stratified splits
        split_generator = fold.split(train_data, target_data)
        test_fold = np.full(len(train_data), -1)
        counter = 0
        for _, test_indices in split_generator:
            test_fold[test_indices] = counter
            counter += 1
        return PredefinedSplit(test_fold)

    @classmethod
    def _get_discretized(cls, target_data: pd.Series, bin_count: int = DEFAULT_BIN_COUNT) -> np.ndarray:
        discretizer = KBinsDiscretizer(n_bins=bin_count, encode="ordinal", strategy="quantile")
        target_data = discretizer.fit_transform(target_data.to_numpy().reshape(-1, 1))[:, 0]
        return target_data
