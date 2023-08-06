""""This module includes ModellingReductionSetttings class."""

from organon.afe.domain.modelling.businessobjects.target_file_record_collection import TargetFileRecordCollection
from organon.afe.domain.modelling.businessobjects.transaction_file_record_collection import \
    TransactionFileRecordCollection
from organon.afe.domain.settings.record_source import RecordSource


class ModellingReductionSettings:
    """Settings for afe column elimination in modelling"""

    def __init__(self):
        self.target_record_source: RecordSource = None
        self.target_record_source_index: int = None
        self.target_file_record_collection: TargetFileRecordCollection = None
        self.trx_file_record_collection: TransactionFileRecordCollection = None
        self.num_threads: int = None
