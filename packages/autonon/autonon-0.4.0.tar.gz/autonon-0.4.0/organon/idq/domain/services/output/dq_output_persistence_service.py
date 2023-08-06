"""Includes DqCalculationPersistenceService class."""
from organon.fl.serialization.serialization_helper import serialize_to_file, deserialize_from_file
from organon.idq.core.dq_constants import DqConstants
from organon.idq.domain.businessobjects.dq_calculation_output import DqCalculationOutput


class DqOutputPersistenceService:
    """Class for persisting dq outputs"""

    @classmethod
    def save_calculation_to_file(cls, calculation_output: DqCalculationOutput, location: str):
        """Saves calculation result to given location(file)"""
        serialize_to_file(calculation_output, location, secret_key=DqConstants.get_secret_key())

    @classmethod
    def load_calculation_from_file(cls, location: str, secret_key: str) -> DqCalculationOutput:
        """Loads calculation result from given location(file)"""
        return deserialize_from_file(location, secret_key=secret_key)
