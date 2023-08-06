"""Includes AfeFeature class"""
from organon.afe.domain.modelling.businessobjects.afe_column import AfeColumn
from organon.afe.domain.modelling.businessobjects.base_afe_feature import BaseAfeFeature


class AfeFeature(BaseAfeFeature[AfeColumn]):
    """Afe feature information class"""
