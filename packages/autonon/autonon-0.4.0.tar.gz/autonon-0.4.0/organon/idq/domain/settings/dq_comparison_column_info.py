"""Includes DqComparisonColumnInfo class."""


class DqComparisonColumnInfo:
    """Dq comparison column settings."""

    def __init__(self):
        self.column_name: str = None
        self.benchmark_horizon: int = None
        self.duplicate_column_control: bool = None
