"""Includes DqBaseCalculationParameters class."""
from typing import TypeVar, Generic, List

from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.idq.domain.businessobjects.dq_calculation_result import DqCalculationResult
from organon.idq.domain.settings.abstractions.dq_base_input_source_settings import DqBaseInputSourceSettings
from organon.idq.domain.settings.dq_column_metadata import DqColumnMetadata

InputSourceSettingsType = TypeVar("InputSourceSettingsType", bound=DqBaseInputSourceSettings)


class DqBaseCalculationParameters(Generic[InputSourceSettingsType]):
    """Base calculation settings for all source types"""

    def __init__(self):
        self.calculation_name: str = None
        self.input_source_settings: InputSourceSettingsType = None
        self.max_nominal_cardinality_count: int = None
        self.outlier_parameter: float = None
        self.column_dq_metadata_list: List[DqColumnMetadata] = None
        self.use_population_nominal_stats: bool = None
        self.is_existing_calculation: bool = None
        self.existing_result: DqCalculationResult = None
        self.nominal_column_types: List[ColumnNativeType] = None
