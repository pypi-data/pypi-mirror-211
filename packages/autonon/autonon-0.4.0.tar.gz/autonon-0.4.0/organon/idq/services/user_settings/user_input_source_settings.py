"""Includes UserInputSourceSettings class."""
from typing import Union, List, Callable

import pandas as pd

from organon.idq.services.user_settings.user_db_obj_locator import UserDbObjLocator


class UserInputSourceSettings:
    """Input source settings user class"""

    def __init__(self):
        self.source: Union[UserDbObjLocator, str, pd.DataFrame] = None
        self.name: str = None
        self.sampling_ratio: float = None
        self.max_num_of_samples: int = None
        self.number_of_rows_per_step: int = None
        self.csv_separator: str = None
        self.where_clause: str = None
        self.date_columns: List[str] = None
        self.filter_callable: Callable = None
