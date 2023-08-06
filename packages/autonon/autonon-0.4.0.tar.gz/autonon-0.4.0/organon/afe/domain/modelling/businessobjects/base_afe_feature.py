"""Includes BaseAfeFeature class"""
from typing import Generic, TypeVar

from organon.afe.domain.modelling.businessobjects.afe_column import AfeColumn

AfeColumnType = TypeVar("AfeColumnType", bound=AfeColumn)


class BaseAfeFeature(Generic[AfeColumnType]):
    """Base Afe feature information class"""

    def __init__(self, afe_column: AfeColumnType):
        self.feature_name: str = None
        self.afe_column = afe_column
