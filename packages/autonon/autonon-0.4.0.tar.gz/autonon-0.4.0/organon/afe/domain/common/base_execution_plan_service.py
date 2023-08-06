"""
This module includes ExecutionPlanService class
"""
from typing import Dict

from organon.afe.domain.common.runtime_stats_service import RuntimeStatsService
from organon.afe.domain.modelling.businessobjects.target_file_record_collection import TargetFileRecordCollection
from organon.afe.domain.modelling.businessobjects.transaction_file_record_collection import \
    TransactionFileRecordCollection
from organon.afe.domain.settings.afe_algorithm_settings import AfeAlgorithmSettings
from organon.afe.domain.settings.feature_generation_settings import FeatureGenerationSettings
from organon.afe.domain.settings.record_source import RecordSource


# pylint: disable=no-self-use
# pylint: disable=unused-argument

class BaseExecutionPlanService:
    """
    Class for estimating remaining time and plan of the service
    """
    GETTING_TARGETS_KEY = 'Getting Targets'
    DECIDE_DIM_QTY_COL_KEY = 'Deciding dim and qty columns'
    CREATE_DISTINCT_ENTITIES_KEY = 'Creating dist. entities table'
    READ_TRX_FILE_KEY = 'Reading trx file'
    REDUCE_COLUMNS_KEY = 'Reducing columns'
    EXTRACT_ALL_VARS_KEY = 'Extracting all variables'
    OUTPUT_KEY = 'Output'

    def __init__(self):
        """
        Initializes object with settings
        """
        self.iteration_count = None
        self.total_reduction_loop = None
        self._runtime_stats_service = RuntimeStatsService()

    def get_runtime_statistics(self):
        """returns recorded runtime statistics"""
        return self._runtime_stats_service.runtime_statistics

    def start_recording_runtime_stats(self, interval_in_seconds: float = 1):
        """Starts recording runtime statistics"""
        self._runtime_stats_service.start_recording_runtime_stats(interval_in_seconds)

    def stop_recording_runtime_stats(self):
        """Stops recording runtime statistics"""
        self._runtime_stats_service.stop_recording_runtime_stats()

    def add_df_builder_statistic(self, target_count, trx_count, d_count, date_col_name, generated_feature, exec_time):
        """
        Adds df_builder statistics
        :param target_count: target count
        :param trx_count: trx count
        :param d_count: dimension count
        :param date_col_name: name of date column corresponding to current statistic
        :param generated_feature: generated features
        :param exec_time: time spent
        """

    def add_unsupervised_statistic(self, column_count, bin_count, record_count, r_factor, selected_count, exec_time):
        """
        Adds unsupervised statistics
        :param column_count: column count
        :param bin_count: bin count
        :param record_count: record count
        :param r_factor: r factor
        :param selected_count: selected count
        :param exec_time: time spent
        """

    def add_supervised_statistic(self, record_count, column_count, exec_time):
        """
        Adds Supervised model statistics
        :param record_count: record count
        :param column_count: column count
        :param exec_time: time past
        """

    def save_statistics(self):
        """
        Saves statistics according to type
        """

    def set_collections(self,
                        trx_collection: TransactionFileRecordCollection,
                        records_per_file: Dict[RecordSource, TargetFileRecordCollection]):
        """
        Sets collections and initializes estimations
        :param trx_collection: trx collections
        :param records_per_file: targets
        """

    def start_get_targets(self):
        """Add start time for reading targets to runtime statistics as event"""
        self._add_event_to_runtime_statistics(self.GETTING_TARGETS_KEY)

    def complete_get_targets(self, exec_time):
        """
        Moves get_targets from to_do_map to completed map with time
        :param exec_time: time past
        """

    def start_create_distinct_entities_table(self):
        """Add start time for creating distinct entities table to runtime statistics as event"""

    def complete_create_distinct_entities_table(self, exec_time):
        """
        Moves create_distinct_entities_table from to_do_map to completed map with time
        :param exec_time: time past
        """

    def start_decide_columns(self):
        """Add start time for deciding dim-qty columns to runtime statistics as event"""
        self._add_event_to_runtime_statistics(self.DECIDE_DIM_QTY_COL_KEY)

    def complete_decide_columns(self, exec_time):
        """
        Moves decide_columns from to_do_map to completed map with time
        :param exec_time: time past
        """

    def start_trx_file(self):
        """Add start time for reading transaction file to runtime statistics as event"""
        self._add_event_to_runtime_statistics(self.READ_TRX_FILE_KEY)

    def complete_trx_file(self, exec_time):
        """
        Moves trx_file from to_do_map to completed map with time
        :param exec_time: time past
        """

    def start_reduce(self):
        """Add start time for reducing columns to runtime statistics as event"""
        self._add_event_to_runtime_statistics(self.REDUCE_COLUMNS_KEY)

    def complete_reduce(self, exec_time):
        """
        Moves reduce from to_do_map to completed map with time
        :param exec_time: time past
        """

    def start_extracting(self):
        """Add start time for extracting all variables to runtime statistics as event"""

    def complete_extracting(self, exec_time):
        """
        Moves extracting from to_do_map to completed map with time
        :param exec_time: time past
        """

    def start_output(self):
        """Add start time for generating/writing outputs to runtime statistics as event"""
        self._add_event_to_runtime_statistics(self.OUTPUT_KEY)

    def complete_output(self, exec_time):
        """
        Moves output from to_do_map to completed map with time
        :param exec_time: time past
        """

    def calculate_reduce_time(self):
        """
        Calculates the total time for reduce
        """

    def calculate_calibrated_reduce_time(self, record_source, order: int,
                                         dimension_column, df_time, model_time):
        """
        Returns calibrated estimation for reduce
        :param record_source: current target source
        :param dimension_column: current dimension
        :param df_time: time past for current iteration
        :param model_time: time past for current iteration
        :return: calibrated time for rest of the iterations
        """

    def get_plan(self):
        """
        Returns the plan

        :return: returns the plan
        """
        return None

    @staticmethod
    def log_trx_remaining(time_past: float, record_fetched: int, fetch_failure: int, record_count: int):
        """
        Logs the remaining info of fetching trx
        :param time_past: time past until log
        :param record_fetched: record fetched successfully
        :param fetch_failure: record failed
        :param record_count: total records
        """

    @staticmethod
    def get_column_count_per_dimension(algorithm_settings: AfeAlgorithmSettings,
                                       feature_generation_setting: FeatureGenerationSettings):
        """
        Returns estimated columns to be generated per dimension
        :param feature_generation_setting:
        :param algorithm_settings: settings
        :return: estimation per dimension
        """

    def _add_event_to_runtime_statistics(self, key: str):
        self._runtime_stats_service.add_event(key)
