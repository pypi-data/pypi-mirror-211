"""
This module includes AfeDataSettings class.
"""
from typing import List, Generic, TypeVar

from organon.afe.domain.common.reader_helper import get_values_from_kwargs
from organon.afe.domain.enums.record_source_type import RecordSourceType
from organon.afe.domain.settings.auto_column_decider_settings import AutoColumnDeciderSettings
from organon.afe.domain.settings.base_trx_descriptor import BaseTrxDescriptor
from organon.afe.domain.settings.record_source import RecordSource
from organon.afe.domain.settings.target_descriptor import TargetDescriptor

T = TypeVar("T", bound=BaseTrxDescriptor)


class BaseAfeDataSettings(Generic[T]):
    """
    Stores data source settings for AfeModellingSettings
    """
    ATTR_DICT = {
        "trx_descriptor": BaseTrxDescriptor,
        "target_descriptor": TargetDescriptor,
        "auto_column_decider_settings": AutoColumnDeciderSettings,
        "target_record_source_list": List[RecordSource],
        "max_number_of_target_samples": int,
        "max_number_of_transaction_samples": int,
    }

    def __init__(self, **kwargs):
        self.trx_descriptor: T = None
        self.target_descriptor: TargetDescriptor = None
        self.auto_column_decider_settings: AutoColumnDeciderSettings = None
        self.target_record_source_list: List[RecordSource] = None
        self.max_number_of_target_samples: int = None
        self.max_number_of_transaction_samples: int = None

        get_values_from_kwargs(self, self.ATTR_DICT, kwargs)

    def is_homogenous(self) -> bool:
        """checks if all target record sources have the same connection name as the transaction record source"""
        trx_source = self.trx_descriptor.modelling_raw_input_source
        if trx_source.get_type() != RecordSourceType.DATABASE:
            return False
        for record_source in self.target_record_source_list:  # pylint: disable=not-an-iterable
            if record_source.get_type() != RecordSourceType.DATABASE or \
                    record_source.source.connection_name != trx_source.source.connection_name:
                return False
        return True
