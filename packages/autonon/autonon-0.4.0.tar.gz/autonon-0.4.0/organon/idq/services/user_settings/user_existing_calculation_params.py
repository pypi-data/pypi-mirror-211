"""Includes UserExistingCalculationParams"""
from organon.idq.domain.businessobjects.dq_calculation_output import DqCalculationOutput


class UserExistingCalculationParams:
    """Stores existing calculation parameters entered by user"""
    def __init__(self, calculation_output: DqCalculationOutput, calculation_name: str):
        self.calculation_output: DqCalculationOutput = calculation_output
        self.calculation_name = calculation_name
