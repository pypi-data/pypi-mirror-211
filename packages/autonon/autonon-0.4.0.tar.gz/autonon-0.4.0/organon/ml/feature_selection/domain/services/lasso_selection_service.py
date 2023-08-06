"""Includes LassoSelectionService class."""
import pandas as pd
from sklearn.linear_model import Lasso

from organon.ml.common.enums.target_type import TargetType
from organon.ml.feature_selection.domain.objects.lasso_selection_output import LassoSelectionOutput
from organon.ml.feature_selection.domain.objects.settings.lasso_selection_settings import LassoSelectionSettings
from organon.ml.feature_selection.domain.services.base_feature_selection_service import SelectionRunSettings
from organon.ml.feature_selection.domain.services.base_supervised_feature_selection_service import \
    BaseSupervisedFeatureSelectionService


class LassoSelectionService(BaseSupervisedFeatureSelectionService[LassoSelectionSettings, LassoSelectionOutput]):
    """Service class for Lasso Selection"""

    @classmethod
    def _validate_settings(cls, settings: LassoSelectionSettings):
        if settings.target_type not in [TargetType.BINARY, TargetType.SCALAR]:
            raise ValueError("Feature selection with Lasso works only for BINARY or SCALAR targets")

    @classmethod
    def _run(cls, run_settings: SelectionRunSettings) -> LassoSelectionOutput:
        settings: LassoSelectionSettings = run_settings.settings
        data = run_settings.data
        target = cls._get_target_data_as_series_of_numbers(settings)

        estimator_args = {} if settings.lasso_args is None else settings.lasso_args
        lasso = Lasso(**estimator_args)
        lasso.fit(data, target)
        lasso_coef_df_tmp = pd.DataFrame(lasso.coef_, columns=['coef'], index=data.columns)
        lasso_coef_df_tmp.reset_index(inplace=True)
        lasso_coef_df_tmp.columns = ['feature', 'coef']
        keep_list = list(lasso_coef_df_tmp[lasso_coef_df_tmp['coef'] != 0]['feature'].values)

        output = LassoSelectionOutput()
        output.selected_features = keep_list
        return output
