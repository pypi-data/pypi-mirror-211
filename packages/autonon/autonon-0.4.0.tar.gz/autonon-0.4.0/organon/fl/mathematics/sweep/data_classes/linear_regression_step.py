"""Module for LinearRegressionStep"""
from dataclasses import dataclass

from organon.fl.mathematics.sweep.data_classes.linear_regression_results import LinearRegressionResults
from organon.fl.mathematics.sweep.data_classes.selected_attribute import SelectedAttribute


@dataclass
class LinearRegressionStep:
    """Step info for results"""
    step: int
    selected_attribute: SelectedAttribute
    anova: LinearRegressionResults

    def __str__(self) -> str:
        result_string = f"STEP NO: {self.step}\n"
        result_string += "\n"
        result_string += "SELECTED ATTRIBUTE INFORMATION:\n"
        result_string += str(self.selected_attribute)
        result_string += "\n"
        result_string += "ANALYSIS OF VARIANCE AT THIS STEP:\n"
        result_string += str(self.anova)

        return result_string
