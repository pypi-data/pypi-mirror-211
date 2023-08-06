"""Includes helper functions for switching dev_mode on/off"""
from organon.fl.core.helpers import guid_helper
from organon.fl.logging.helpers.log_helper import LogHelper, Levels


def init_dev_mode(module_name: str, log_to_console: bool = True, log_file: str = "application.log"):
    """Initializes development mode."""
    execution_id = guid_helper.new_guid(32)

    LogHelper.set_logger_level(Levels.INFO, module_name)
    if log_to_console:
        LogHelper.add_console_handler(module_name)
    if log_file:
        LogHelper.add_file_handler(log_file, module_name)
    LogHelper.add_global_extra("execution_id", execution_id)
    default_format = "[%(asctime)s] [%(threadName)s] %(levelname)-8s %(module_name)s:%(line_number)s : " \
                     "%(execution_id)s  - %(message)s"
    LogHelper.set_default_formatter_default_format_str(default_format)
