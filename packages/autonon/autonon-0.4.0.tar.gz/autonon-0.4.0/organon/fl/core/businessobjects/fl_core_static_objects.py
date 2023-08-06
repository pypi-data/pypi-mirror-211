"""
This module keeps FlCoreStaticObjects class.
"""
from typing import List

from organon.fl.core.fileoperations import directory_helper
from organon.fl.core.helpers import string_helper
from organon.fl.core.iocutil.ioc_registration_item import IocRegistrationItem


class FlCoreStaticObjects:
    """
    Class for holding ioc registered items, registered connections and application_initialize_called boolean object.
    """
    ioc_registered_items: List[IocRegistrationItem] = None
    application_initialize_called: bool = None

    fl_app_output_directory: str = None

    @staticmethod
    def get_master_output_directory():
        """Returns master output directory for application"""
        FlCoreStaticObjects.set_fl_app_context_from_config()
        if not string_helper.is_null_or_empty(FlCoreStaticObjects.fl_app_output_directory):
            return FlCoreStaticObjects.fl_app_output_directory
        return directory_helper.get_current_directory()

    @staticmethod
    def set_fl_app_context_from_config():
        """Sets fl context settings from config file."""
