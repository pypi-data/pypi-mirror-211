"""Includes DqFullProcessInput class."""
from typing import List, TypeVar, Generic

from organon.idq.domain.settings.abstractions.dq_base_calculation_parameters import DqBaseCalculationParameters
from organon.idq.domain.settings.abstractions.dq_base_comparison_parameters import DqBaseComparisonParameters
from organon.idq.domain.settings.dask_settings import DaskSettings
from organon.idq.domain.settings.dq_notification_settings import DqNotificationSettings
from organon.idq.domain.settings.dq_output_settings import DqOutputSettings

T1 = TypeVar("T1", bound=DqBaseCalculationParameters)
T2 = TypeVar("T2", bound=DqBaseComparisonParameters)


class DqFullProcessInput(Generic[T1, T2]):
    """All settings required for a full DQ process."""

    def __init__(self):
        self.calculation_parameters: List[T1] = None
        self.comparison_parameters: T2 = None
        self.use_supplied_calcs_as_comp_inputs: bool = None
        self.notification_settings: DqNotificationSettings = None
        self.output_settings: DqOutputSettings = None
        self.dask_settings: DaskSettings = None
