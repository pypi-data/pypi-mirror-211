"""Includes UserFeatureReductionSettings class."""


class UserFeatureReductionSettings:
    """Settings for user feature reduction settings"""

    def __init__(self):
        self.data = None
        self.null_ratio_threshold = None
        self.target_type = None
        self.target_column_name = None
        self.performance_metric = None
        self.univariate_performance_threshold = None
        self.correlation_threshold = None
        self.included_reduction_types = None
        self.nunique_count = None
        self.random_state = None
        self.excluded_columns = None
