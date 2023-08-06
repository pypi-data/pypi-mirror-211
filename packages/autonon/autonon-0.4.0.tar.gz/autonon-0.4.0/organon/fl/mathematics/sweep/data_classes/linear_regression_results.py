"""Module for LinearRegressionResults"""
import math
from dataclasses import dataclass


@dataclass
class LinearRegressionResults:
    """Statistical results of the linear regression algorithm"""
    parameters = None
    sample_size = None
    bias_dict = {}
    r_square = None
    adjusted_r_square = None
    model_degrees_of_freedom = None
    error_degrees_of_freedom = None
    total_sum_of_squares = None
    explained_sum_of_squares = None
    residual_sum_of_squares = None
    mean_square_error = None
    mean_square_regression = None
    f_statistics = None
    f_statistics_p_value = None

    # pylint: disable=unsubscriptable-object
    def __str__(self) -> str:
        result_string = f"Number of samples: {self.sample_size}\n"
        result_string += f"RSquared: {self.r_square}\n"
        result_string += f"Adjusted-RSquared: {self.adjusted_r_square}\n"
        result_string += f"Standard Error-of-Regression: {math.sqrt(self.mean_square_error)}\n"
        result_string += "\n"
        result_string += "\n"
        result_string += f"Number of samples: {self.sample_size}\n"
        result_string += "\n"
        result_string += "Analysis of Variance:\n"
        result_string += "\n"
        result_string += f"               {'DF':<15}{'Sum of Squares':<25}{'Mean Square':<25}\n"
        result_string += f"{'Regression':<15}{self.model_degrees_of_freedom:<15,G}" \
                         f"{self.explained_sum_of_squares:<25,E}{self.mean_square_regression:<25,E}\n"
        result_string += f"{'Residuals':<15}{(self.sample_size- self.model_degrees_of_freedom - 1):<15,G}" \
                         f"{self.residual_sum_of_squares:<25,E}{self.mean_square_error:<25,E}\n"
        result_string += "\n"
        result_string += "\n"
        result_string += "\n"
        result_string += f"{'NAME':<25}{'B':<20}{'SEB':<20}{'T':<20}{'VIF':<20}\n"
        result_string += f"{'CONSTANT':<25}{round(self.bias_dict['estimate'],6):<20}{float('nan'):<20}" \
                         f"{float('nan'):<20}{float('nan'):<20}\n"

        for key in self.parameters:  # pylint: disable=not-an-iterable
            result_string += f"{key:<25}{round(self.parameters[key].estimate, 6):<20}" \
                             f"{ round(self.parameters[key].standard_error,6):<20}" \
                             f"{round(self.parameters[key].test_statistic, 6):<20}" \
                             f"{round(self.parameters[key].vif, 6):<20}\n"

        return result_string
