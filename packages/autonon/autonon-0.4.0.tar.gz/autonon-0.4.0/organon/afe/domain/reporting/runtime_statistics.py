"""
This module includes RuntimeStatistics class.
"""
from datetime import datetime
from typing import Dict


class RuntimeStatistics:
    """Runtime statistics."""
    def __init__(self):
        self.execution_time: float = None
        self.user_cpu_time: float = None
        self.system_cpu_time: float = None
        self.memory_usage: Dict[datetime, float] = {}
        self.cpu_usage: Dict[datetime, float] = {}
        self.event_times: Dict[str, datetime] = {}
