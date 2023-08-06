"""
This module includes MultiTargetEntityContainer class.
"""
import secrets
from typing import Dict, List

from organon.afe.domain.common import afe_date_helper
from organon.afe.domain.enums.date_resolution import DateResolution
from organon.afe.domain.modelling.businessobjects.target_file_record_collection import TargetFileRecordCollection
from organon.afe.domain.settings.record_source import RecordSource
from organon.fl.core.businessobjects.date_interval import DateInterval
from organon.fl.core.enums.date_interval_type import DateIntervalType
from organon.fl.mathematics import constants


class MultiTargetEntityContainer:
    """
    Container for record collections in every target file record source
    """

    def __init__(self):
        self.__records_per_file: Dict[RecordSource, TargetFileRecordCollection] = {}
        self.__unique_entity_list: List[str] = []

    @property
    def records_per_file(self) -> Dict[RecordSource, TargetFileRecordCollection]:
        """Returns value of private attribute '__records_per_file'"""
        return self.__records_per_file

    @property
    def unique_entity_list(self) -> List[str]:
        """Returns value of private attribute '__unique_entity_list'"""
        return self.__unique_entity_list

    def add(self, source: RecordSource, collection: TargetFileRecordCollection):
        """
        Adds new source-collection pair to records_per_file dictionary
        :param source:
        :type source: RecordSource
        :param collection:
        :type collection: TargetFileRecordCollection
        """
        self.records_per_file[source] = collection

    def remove(self, source: RecordSource):
        """
        Remove source from records_per_file dictionary.
        :param source:
        :type source: RecordSource
        """
        if source in self.records_per_file:
            self.records_per_file.pop(source)

    def unify_entity_list(self, max_sample_size: int):
        """
        Gets unique entity samples from every record source and stores in '__unique_entity_list'
        :param max_sample_size: Maximum number of samples to get from a record source.
        :type max_sample_size: int
        """
        rand = secrets.SystemRandom()
        tmp_list = []
        for collection in self.records_per_file.values():
            tmp_list.extend(collection.get_sampled_unique_entities(rand, max_sample_size))

        self.__unique_entity_list = list(set(tmp_list))

    def get_date_interval_per_entity(self, resolution: DateResolution, max_horizon: int, date_offset: int) -> \
            Dict[str, DateInterval]:
        """
         returns Dictionary where keys are entities and values are DateIntervals
        """
        func_bottom = afe_date_helper.get_date_subtraction_func(resolution, max_horizon + date_offset)
        func_top = afe_date_helper.get_date_subtraction_func(resolution, date_offset)
        tmp: Dict[str, List[int]] = {}
        for collection in self.records_per_file.values():
            for index in range(collection.actual_record_count):
                _id = collection.entities[index]
                event_date = collection.event_dates[index]
                if _id not in tmp:
                    tmp[_id] = [constants.INT_MAX, constants.INT_MIN]
                bottom = func_bottom(event_date)
                top = func_top(event_date)
                if bottom < tmp[_id][0]:
                    tmp[_id][0] = bottom
                if event_date > tmp[_id][1]:
                    tmp[_id][1] = top
        return {key: DateInterval(value[0], value[1], DateIntervalType.CLOSED_CLOSED) for key, value in tmp.items()}
