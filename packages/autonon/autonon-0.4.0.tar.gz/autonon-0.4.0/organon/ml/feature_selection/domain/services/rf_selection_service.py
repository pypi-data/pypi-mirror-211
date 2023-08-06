"""Includes RFSelectionService class"""
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

from organon.ml.common.enums.target_type import TargetType
from organon.ml.feature_selection.domain.objects.rf_selection_output import RFSelectionOutput
from organon.ml.feature_selection.domain.objects.settings.rf_selection_settings import RFSelectionSettings
from organon.ml.feature_selection.domain.services.base_feature_selection_service import SelectionRunSettings
from organon.ml.feature_selection.domain.services.base_supervised_feature_selection_service import \
    BaseSupervisedFeatureSelectionService


class RFSelectionService(BaseSupervisedFeatureSelectionService[RFSelectionSettings, RFSelectionOutput]):
    """Service class for RFSelection"""

    @classmethod
    def _validate_settings(cls, settings: RFSelectionSettings):
        cls._validate_original_data_for_sweep(settings.data)

    @classmethod
    def _run(cls, run_settings: SelectionRunSettings) -> RFSelectionOutput:
        settings: RFSelectionSettings = run_settings.settings
        data = run_settings.data
        estimator_args = {} if settings.rf_args is None else settings.rf_args
        rf_estimator = RandomForestClassifier(**estimator_args) \
            if settings.target_type in [TargetType.BINARY, TargetType.MULTICLASS] \
            else RandomForestRegressor(**estimator_args)
        rf_estimator.fit(data, settings.target)
        imp_df = pd.DataFrame(rf_estimator.feature_importances_, columns=['importance'], index=data.columns)
        imp_df = imp_df.sort_values(by="importance", ascending=False)
        num_features = settings.num_features
        if num_features is None:
            num_features = len(cls._get_features_with_sweep(data, settings.sweep_args))
        selected_features = imp_df.index[:num_features].to_list()
        output = RFSelectionOutput()
        output.selected_features = selected_features
        return output
