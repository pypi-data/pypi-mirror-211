"""Includes BaseUserCalculationParams class."""

from organon.idq.services.user_settings.user_input_source_settings import UserInputSourceSettings


class BaseUserCalculationParams:
    """Base calculation settings user class"""

    def __init__(self, calc_name, input_source_settings, max_nom_card_count, outlier_param,
                 use_pop_nom_stats):
        self.calculation_name: str = calc_name
        self.input_source_settings: UserInputSourceSettings = input_source_settings
        self.max_nominal_cardinality_count: int = max_nom_card_count
        self.outlier_parameter: float = outlier_param
        self.use_population_nominal_stats: bool = use_pop_nom_stats
