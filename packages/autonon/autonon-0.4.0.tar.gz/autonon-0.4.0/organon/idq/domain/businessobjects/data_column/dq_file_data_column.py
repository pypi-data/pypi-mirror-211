"""Includes DqFileDataColumn class."""
import numpy as np

from organon.idq.domain.businessobjects.data_column.dq_data_column import DqDataColumn


class DqFileDataColumn(DqDataColumn):
    """DqDataColumn corresponding to a column in a csv file"""

    def __init__(self):
        super().__init__()
        self.col_np_dtype: np.dtype = None
