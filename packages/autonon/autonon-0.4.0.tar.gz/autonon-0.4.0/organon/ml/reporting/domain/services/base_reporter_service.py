"""Includes BaseReporterService class"""
import abc
from typing import TypeVar, Generic

import pandas as pd

from organon.ml.reporting.domain.objects.base_report import BaseReport
from organon.ml.reporting.settings.objects.reporter_settings import ReporterSettings

ReportType = TypeVar("ReportType", bound=BaseReport)


class BaseReporterService(Generic[ReportType], metaclass=abc.ABCMeta):
    """Base class for reporter services"""

    @classmethod
    @abc.abstractmethod
    def execute(cls, settings: ReporterSettings) -> ReportType:
        """Executes reporting and returns report"""

    @classmethod
    def _get_row_count(cls, data: pd.DataFrame):
        return len(data)
