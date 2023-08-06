"""
This module includes MultiTargetEntityContainerService class.
"""
from typing import List

from organon.afe.dataaccess.services.target_file_record_repository import TargetFileRecordRepository
from organon.afe.domain.modelling.businessobjects.multi_target_entity_container import MultiTargetEntityContainer
from organon.afe.domain.settings.record_source import RecordSource
from organon.afe.domain.settings.target_descriptor import TargetDescriptor
from organon.fl.core.executionutil import parallel_execution_helper


class MultiTargetEntityContainerService:
    """
    Creates a MultiTargetEntityContainer using an AfeModellingSettings instance.
    """

    def __init__(self, target_record_source_list: List[RecordSource], target_descriptor: TargetDescriptor,
                 rejected_target_classes: List[str] = None, is_scoring=False):
        self.__target_record_source_list = target_record_source_list
        self.__target_descriptor = target_descriptor
        self.__container: MultiTargetEntityContainer = None
        self.rejected_target_classes = rejected_target_classes
        self._is_scoring = is_scoring

    @property
    def container(self):
        """Returns value of private attribute '__container'"""
        return self.__container

    def execute(self):
        """
        Sets 'container' value using 'settings'.
        """
        descriptor = self.__target_descriptor

        def inner(record_source):
            repository = self._get_repository(record_source, descriptor, self.rejected_target_classes, self._is_scoring)
            collection = repository.read()
            self.__container.add(record_source, collection)

        self.__container = MultiTargetEntityContainer()

        record_source_list = self.__target_record_source_list
        num_threads = min(len(record_source_list), 25)
        parallel_execution_helper.execute_parallel(record_source_list, inner, num_jobs=num_threads, backend="threading")

    def _get_repository(self, record_source, target_descriptor, rejected_target_classes,
                        is_scoring: bool = False) -> TargetFileRecordRepository:
        # pylint: disable=no-self-use
        return TargetFileRecordRepository(record_source, target_descriptor, rejected_target_classes, is_scoring)
