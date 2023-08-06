"""Incudes DataEntity enum definition."""
from enum import Enum


class DataEntityType(Enum):
    """db data entity types"""
    TABLE = 1
    COLUMN = 2
