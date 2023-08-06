"""todo"""
from organon.idq.domain.businessobjects.dq_data_column_collection import DqDataColumnCollection


class DataSourceStatistics:
    """todo"""

    def __init__(self):
        self.row_count: int = None
        self.size_in_bytes: int = None
        self.data_column_collection: DqDataColumnCollection = None
