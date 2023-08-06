"""Includes UserPartitionInfo class."""
from typing import Union, List

from organon.idq.services.user_settings.user_date_value_definition import UserDateValueDefinition


class UserPartitionInfo:
    """User settings class for PartitionInfo."""

    def __init__(self):
        self.column_name: str = None
        self.column_values: Union[List[UserDateValueDefinition], List[float], List[str]] = None
