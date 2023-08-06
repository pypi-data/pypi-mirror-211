"""Includes ColumnMetadata class."""
from typing import List


class DqColumnMetadata:
    """Column metadata settings"""

    def __init__(self):
        self.column_name: str = None
        self.default_values: List[str] = None
        self.inclusion_flag: bool = None
