"""
This module includes IdqApplicationOperations class.
"""
import threading

from organon.fl.generic.interaction.fl_initializer import FlInitializer


class IdqApplicationOperations:
    """Idq Application Operations"""

    APPLICATION_INITIALIZED = False
    __INITIALIZATION_LOCK = threading.Lock()

    @classmethod
    def initialize_app(cls):
        """Initializes application."""
        with IdqApplicationOperations.__INITIALIZATION_LOCK:
            if not IdqApplicationOperations.APPLICATION_INITIALIZED:
                cls._initialize_fl()
                IdqApplicationOperations.register_types()
                IdqApplicationOperations.APPLICATION_INITIALIZED = True

    @classmethod
    def _initialize_fl(cls):
        FlInitializer.application_initialize()

    @classmethod
    def register_types(cls):
        """Registers types to IOC"""
        # todo
