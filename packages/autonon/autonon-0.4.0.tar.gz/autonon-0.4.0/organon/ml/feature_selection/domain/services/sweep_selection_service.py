"""Includes SweepSelectionService class"""
from organon.ml.feature_selection.domain.objects.settings.sweep_selection_settings import SweepSelectionSettings
from organon.ml.feature_selection.domain.objects.sweep_selection_output import SweepSelectionOutput
from organon.ml.feature_selection.domain.services.base_feature_selection_service import SelectionRunSettings
from organon.ml.feature_selection.domain.services.base_unsupervised_feature_selection_service import \
    BaseUnsupervisedFeatureSelectionService


class SweepSelectionService(BaseUnsupervisedFeatureSelectionService[SweepSelectionSettings, SweepSelectionOutput]):
    """Service class for SweepSelection"""

    @classmethod
    def _validate_settings(cls, settings: SweepSelectionSettings):
        cls._validate_original_data_for_sweep(settings.data)

    @classmethod
    def _run(cls, run_settings: SelectionRunSettings) -> SweepSelectionOutput:
        settings: SweepSelectionSettings = run_settings.settings
        sweep_args = cls._get_sweep_args(settings)
        selected_features = cls._get_features_with_sweep(run_settings.data, sweep_args)
        output = SweepSelectionOutput()
        output.selected_features = selected_features
        return output

    @classmethod
    def _get_sweep_args(cls, settings: SweepSelectionSettings):
        sweep_args = {}
        if settings.bin_count is not None:
            sweep_args["bin_count"] = settings.bin_count
        if settings.r_factor is not None:
            sweep_args["r_factor"] = settings.r_factor
        if settings.random_state is not None:
            sweep_args["random_state"] = settings.random_state
        if settings.max_col_count is not None:
            sweep_args["max_col_count"] = settings.max_col_count
        if settings.n_threads is not None:
            sweep_args["n_threads"] = settings.n_threads
        return sweep_args
