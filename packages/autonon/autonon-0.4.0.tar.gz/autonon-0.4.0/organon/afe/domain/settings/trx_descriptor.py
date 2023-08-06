"""
This module includes TransactionFileDescriptor class.
"""

from organon.afe.domain.common.reader_helper import get_values_from_kwargs
from organon.afe.domain.settings.base_trx_descriptor import BaseTrxDescriptor
from organon.afe.domain.settings.feature_generation_settings import FeatureGenerationSettings


class TrxDescriptor(BaseTrxDescriptor):
    """
    Class for information about transaction file or database table
    """
    ATTR_DICT = {
        "feature_gen_setting": FeatureGenerationSettings
    }
    ATTR_DICT.update(BaseTrxDescriptor.ATTR_DICT)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.feature_gen_setting: FeatureGenerationSettings = None

        get_values_from_kwargs(self, self.ATTR_DICT, kwargs)

    def get_all_dimension_and_quantity_columns(self):
        """Returns sets of all dimension and quantity columns defined in date column settings"""
        all_d_cols = set()
        all_q_cols = set()
        all_d_cols.update(self.feature_gen_setting.dimension_columns)
        all_q_cols.update(self.feature_gen_setting.quantity_columns)
        return all_d_cols, all_q_cols
