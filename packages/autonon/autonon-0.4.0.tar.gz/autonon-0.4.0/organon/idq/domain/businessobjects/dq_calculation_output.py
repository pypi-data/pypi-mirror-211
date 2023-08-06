"""Includes DqCalculationOutput class."""
from organon.idq.domain.businessobjects.dq_calculation_result import DqCalculationResult
from organon.idq.domain.settings.abstractions.dq_base_calculation_parameters import DqBaseCalculationParameters


class DqCalculationOutput:
    """Stores dq calculation results with its parameters and extra info of execution"""

    def __init__(self):
        self.calculation_parameters: DqBaseCalculationParameters = None
        self.calculation_result: DqCalculationResult = None
