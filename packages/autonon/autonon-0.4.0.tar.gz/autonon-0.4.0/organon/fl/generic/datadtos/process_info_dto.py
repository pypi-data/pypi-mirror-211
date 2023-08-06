"""
This module keeps the ProcessInfoDto class.
"""


class ProcessInfoDto:
    """
    This class keeps the information of process.
    """
    def __init__(self, process_name: str, process_id: int):
        self.process_name = process_name
        self.process_id = process_id
