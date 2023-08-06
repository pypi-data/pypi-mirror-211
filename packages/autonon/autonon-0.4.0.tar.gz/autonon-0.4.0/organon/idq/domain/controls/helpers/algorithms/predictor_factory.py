""" This module includes PredictorFactory class """
from organon.idq.domain.controls.helpers.algorithms.random_forest_predictor import RandomForestPredictor
from organon.idq.domain.enums.dq_pred_algorithm_type import DqPredAlgorithmType


class PredictorFactory:
    """ Class for PredictorFactory"""

    @staticmethod
    def get_predictor(predictor: DqPredAlgorithmType):
        """ :returns predictor instance according to its type """
        if predictor == DqPredAlgorithmType.RANDOM_FOREST_REG:
            return RandomForestPredictor()
        raise NotImplementedError
