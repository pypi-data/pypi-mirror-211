"""Includes helper functions for validation"""
from organon.ml.common.enums.target_type import TargetType
from organon.ml.modelling.algorithms.core.enums.modeller_type import ModellerType


def validate_get_target_type(modeller_type: ModellerType, target_type: TargetType):
    """Validates target type for given modeller type"""
    if modeller_type == ModellerType.CLASSIFIER:
        if target_type is None:
            raise ValueError("Target type should be given for classification")
        if target_type not in [TargetType.BINARY, TargetType.MULTICLASS]:
            raise ValueError("Only BINARY and MULTICLASS are accepted as valid target types in classification")
    elif modeller_type == ModellerType.REGRESSOR:
        if target_type is not None and target_type != TargetType.SCALAR:
            raise ValueError("Only SCALAR is accepted as valid target type in regression")
        target_type = TargetType.SCALAR
    return target_type
