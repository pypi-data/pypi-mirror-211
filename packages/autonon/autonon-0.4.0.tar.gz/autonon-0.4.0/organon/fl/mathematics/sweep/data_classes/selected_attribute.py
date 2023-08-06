"""Module for SelectedAttribute"""
from dataclasses import dataclass

from organon.fl.mathematics.sweep.enums import AttributeSelectionStatus, TestStatisticsType


@dataclass
class SelectedAttribute:
    """Selected Attribute info"""
    attribute_name: str
    selection_status: AttributeSelectionStatus
    selection_test_statistics: TestStatisticsType
    selection_statistics: float
    updated_training_performance: float
    updated_validation_performance: float
    performance_change_in_training_set: float
    performance_change_in_validation_set: float

    def __str__(self) -> str:
        result_string = f"Attribute Name: {self.attribute_name}\n"
        result_string += f"Selection Status: {self.selection_status}\n"
        result_string += f"Selection Test Statistics: {self.selection_test_statistics}\n"
        result_string += f"Selection Statistics: {self.selection_statistics}\n"
        result_string += f"Updated Training Performance: {self.updated_training_performance}\n"
        result_string += f"Updated Validation Performance: {self.updated_validation_performance}\n"
        result_string += f"Performance Change In Training-Set: {self.performance_change_in_training_set}\n"
        result_string += f"Performance Change In Validation-Set: {self.performance_change_in_validation_set}\n"

        return result_string
