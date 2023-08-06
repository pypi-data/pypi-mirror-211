"""
This module includes AfeModellingSettings class.
"""
from typing import TypeVar, Generic

from organon.afe.domain.common.reader_helper import get_values_from_kwargs, get_val_from_kwargs
from organon.afe.domain.enums.afe_learning_type import AfeLearningType
from organon.afe.domain.modelling.supervised.afe_supervised_algorithm_settings import AfeSupervisedAlgorithmSettings
from organon.afe.domain.modelling.unsupervised.afe_unsupervised_algorithm_settings import \
    AfeUnsupervisedAlgorithmSettings
from organon.afe.domain.settings.afe_algorithm_settings import AfeAlgorithmSettings
from organon.afe.domain.settings.afe_output_settings import AfeOutputSettings
from organon.afe.domain.settings.afe_process_settings import AfeProcessSettings
from organon.afe.domain.settings.base_afe_data_settings import BaseAfeDataSettings
from organon.afe.domain.settings.base_afe_settings import BaseAfeSettings
from organon.afe.domain.settings.record_source import RecordSource

DS = TypeVar("DS", bound=BaseAfeDataSettings)
OS = TypeVar("OS", bound=AfeOutputSettings)


class BaseAfeModellingSettings(Generic[DS, OS], BaseAfeSettings):
    """
    Modelling Settings for Automated Feature Extraction process
    """
    ATTR_DICT = {
        "process_settings": AfeProcessSettings,
        "afe_learning_type": AfeLearningType,
        "data_source_settings": BaseAfeDataSettings,
        "output_settings": AfeOutputSettings,
        "algorithm_settings": AfeAlgorithmSettings,
        "scoring_target_source": RecordSource,
        "scoring_raw_input_source": RecordSource,
    }

    def __init__(self, **kwargs):
        super().__init__()
        self.output_settings: OS = None
        self.scoring_target_source: RecordSource = None
        self.scoring_raw_input_source: RecordSource = None
        self.afe_learning_type: AfeLearningType = None
        self.algorithm_settings: AfeAlgorithmSettings = None
        self.data_source_settings: DS = None

        get_values_from_kwargs(self, self.ATTR_DICT, kwargs,
                               ["algorithm_settings"])

        if "algorithm_settings" in kwargs:
            if self.afe_learning_type in [AfeLearningType.Supervised.name, AfeLearningType.Supervised]:
                self.algorithm_settings = get_val_from_kwargs(kwargs["algorithm_settings"],
                                                              AfeSupervisedAlgorithmSettings)
            elif self.afe_learning_type in [AfeLearningType.Unsupervised.name, AfeLearningType.Unsupervised]:
                self.algorithm_settings = get_val_from_kwargs(kwargs["algorithm_settings"],
                                                              AfeUnsupervisedAlgorithmSettings)
            else:
                raise ValueError("Invalid afe_learning_type value")
