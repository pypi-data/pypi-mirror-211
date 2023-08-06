"""Includes helper methods for transaction source read."""
from typing import List, Dict

import pandas as pd

from organon.afe.core.businessobjects.afe_static_objects import AfeStaticObjects
from organon.afe.dataaccess.services.transaction_file_record_reader import TransactionFileRecordReader
from organon.afe.domain.settings.afe_algorithm_settings import AfeAlgorithmSettings
from organon.afe.domain.settings.afe_data_settings import AfeDataSettings
from organon.afe.domain.settings.feature_generation_settings import FeatureGenerationSettings
from organon.afe.domain.settings.record_source import RecordSource
from organon.fl.core.businessobjects.date_interval import DateInterval


def get_trx_file_record_reader_for_modelling(
        dimension_columns: List[str], quantity_columns: List[str],
        data_source_settings: AfeDataSettings,
        algorithm_settings: AfeAlgorithmSettings,
        interval_per_entity_per_date_col: Dict[str, Dict[str, DateInterval]],
        unique_entities_list: List[str]):
    """Generates TransactionFileRecordReader instance for modelling using given values"""
    distinct_entities_df = pd.DataFrame({AfeStaticObjects.distinct_entities_entity_column_name: unique_entities_list})
    distinct_entities_record_source = RecordSource(source=distinct_entities_df)

    trx_descriptor = data_source_settings.trx_descriptor

    date_columns = __get_date_columns(trx_descriptor.feature_gen_setting)

    min_max_dates_per_date_col = {}
    date_col = trx_descriptor.feature_gen_setting.date_column
    max_obs_date = trx_descriptor.feature_gen_setting.max_observation_date
    if date_col is not None and max_obs_date is not None:
        min_max_dates_per_date_col[date_col.column_name] = (None, max_obs_date)

    trx_reader = TransactionFileRecordReader(
        data_source_settings.trx_descriptor.modelling_raw_input_source,
        date_columns,
        data_source_settings.trx_descriptor.entity_column_name,
        interval_per_entity_per_date_column=interval_per_entity_per_date_col,
        distinct_entity_source=distinct_entities_record_source,
        entity_source_entity_column=AfeStaticObjects.distinct_entities_entity_column_name,
        dimension_columns=dimension_columns, quantity_columns=quantity_columns,
        min_max_dates_per_date_column=min_max_dates_per_date_col,
        max_number_of_transaction_samples=data_source_settings.max_number_of_transaction_samples,
        reading_settings=trx_descriptor.reading_settings,
        dimension_compression_ratio=algorithm_settings.dimension_compression_ratio,
        dimension_max_cardinality=algorithm_settings.dimension_max_cardinality
    )

    return trx_reader


def __get_date_columns(feature_generation_settings: FeatureGenerationSettings):
    date_columns = {}
    if feature_generation_settings.date_column is not None:
        date_columns[feature_generation_settings.date_column.column_name] = \
            feature_generation_settings.date_column
    return date_columns
