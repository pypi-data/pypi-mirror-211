""" This module includes StabilityFeatureReduction"""
from organon.ml.feature_reduction.domain.enums.feature_reduction_types import FeatureReductionType
from organon.ml.feature_reduction.domain.objects.feature_reduction_output import FeatureReductionOutput
from organon.ml.feature_reduction.domain.reductions.base_feature_reduction import BaseFeatureReduction
from organon.ml.feature_reduction.settings.objects.stability_feature_reduction_settings import \
    StabilityFeatureReductionSettings


class StabilityFeatureReduction(BaseFeatureReduction):
    """StabilityFeatureReduction class"""

    def _execute_reduction(self, settings: StabilityFeatureReductionSettings) -> FeatureReductionOutput:
        output = FeatureReductionOutput()
        output.feature_reduction_type = FeatureReductionType.STABILITY

        included_columns = self._get_included_columns(settings.data, settings.excluded_columns)

        if not included_columns:
            output.reduced_column_list = None
            return output

        reduced_columns = [col for col in included_columns if len(settings.data[col].value_counts()) == 1]

        output.reduced_column_list = reduced_columns
        return output

    def get_description(self) -> str:
        return "Stability Feature Reduction"
