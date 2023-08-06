"""
This module includes AfeColumnDto class.
"""


class AfeColumnDto:
    """
    AfeColumnDto
    """

    def __init__(self):
        self.name: str = None
        self.dimension: str = None
        self.dimension_set: str = None
        self.quantity: str = None
        self.operator: str = None
        self.date_column_name: str = None
        self.time_window: int = None
        self.trend_time_window: int = None
        self.time_resolution: str = None
        self.offset: int = None
