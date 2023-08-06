"""
This module includes AfeOutputSettings class.
"""
from organon.afe.domain.common.reader_helper import get_values_from_kwargs


class AfeOutputSettings:
    """
    Settings for output of Automated Feature Extraction
    """
    ATTR_DICT = {
        "output_folder": str,
        "output_prefix": str,
        "feature_name_prefix": str,
        "enable_write_output": bool,
        "enable_feature_lookup_output_to_csv": bool,
        "return_all_afe_columns": bool,
        "enable_all_feature_lookup_output_to_csv": bool
    }

    def __init__(self, **kwargs):
        self.output_folder: str = None
        self.output_prefix: str = None
        self.feature_name_prefix: str = None

        self.enable_feature_lookup_output_to_csv: bool = None
        self.enable_write_output: bool = None
        self.return_all_afe_columns: bool = None
        self.enable_all_feature_lookup_output_to_csv = None

        get_values_from_kwargs(self, self.ATTR_DICT, kwargs)

    def get_feature_table_name(self) -> str:
        """
        :return: name for feature table
        """
        return f"{self.output_prefix}_FEATURE_DVL"

    def get_feature_lookup_table_name(self) -> str:
        """
        :return: name for feature lookup table
        """
        return f"{self.output_prefix}_LOOKUP"

    def get_all_features_lookup_table_name(self) -> str:
        """
        :return: name for all lookup table
        """
        return f"{self.output_prefix}_ALL_LOOKUP"

    def get_sql_file(self) -> str:
        """
        :return: sql file name
        """
        return f"{self.output_prefix}_SQL"

    def get_distinct_entities_file(self) -> str:
        """
        :return: distinct entity table name
        """
        return f"{self.output_prefix}_DISTINCT_ENTITY_TABLE"
