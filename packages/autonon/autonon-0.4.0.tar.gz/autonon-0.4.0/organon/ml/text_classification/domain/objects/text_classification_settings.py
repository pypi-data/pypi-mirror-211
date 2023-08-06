"""Class for general text classification settings"""
from organon.ml.text_classification.domain.enums.classification_languages import ClassificationLanguages
from organon.ml.text_classification.domain.enums.model_checkpoints import ModelCheckpoints
from organon.ml.text_classification.domain.enums.model_run_type import ModelRunType
from organon.ml.text_classification.domain.objects.grid_search_settings import GridSearchSettings
from organon.ml.text_classification.domain.objects.model_parameter_settings import ModelParameterSettings
from organon.ml.text_classification.domain.objects.optimizer_settings import OptimizerSettings
from organon.ml.text_classification.domain.objects.tokenizer_settings import TokenizerSettings


class TextClassificationSettings:
    """Text Classification Module Settings"""

    def __init__(self, language: ClassificationLanguages, text_column: str = None, target_column: str = None,
                 checkpoint: ModelCheckpoints = ModelCheckpoints.BERT_BASE,
                 mdl_run_type: ModelRunType = ModelRunType.EFFICIENT,
                 mdl_param_settings: ModelParameterSettings = None,
                 opt_settings: OptimizerSettings = None,
                 tokenizer_settings: TokenizerSettings = None,
                 grid_search_settings: GridSearchSettings = None):
        # pylint: disable=too-many-arguments
        self.language = language
        self.text_column = text_column
        self.target_column = target_column
        self.checkpoint: ModelCheckpoints = checkpoint
        self.mdl_run_type = mdl_run_type
        self.mdl_param_settings: ModelParameterSettings = mdl_param_settings \
            if mdl_param_settings is not None else ModelParameterSettings()
        self.opt_settings: OptimizerSettings = opt_settings \
            if opt_settings is not None else OptimizerSettings()
        self.tokenizer_settings: TokenizerSettings = tokenizer_settings \
            if tokenizer_settings is not None else TokenizerSettings()
        self.grid_src_settings: GridSearchSettings = grid_search_settings \
            if grid_search_settings is not None else GridSearchSettings()
