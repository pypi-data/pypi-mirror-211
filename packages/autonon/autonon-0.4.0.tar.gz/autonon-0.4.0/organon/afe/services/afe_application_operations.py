"""
This module includes AfeApplicationOperations class.
"""
import threading

from organon.afe.core.businessobjects.afe_static_objects import AfeStaticObjects
from organon.fl.generic.interaction.fl_initializer import FlInitializer


class AfeApplicationOperations:
    """
    AfeApplicationOperations
    """

    APPLICATION_INITIALIZED = False
    __INITIALIZATION_LOCK = threading.Lock()

    @classmethod
    def initialize_app(cls):
        """Initializes application."""
        with AfeApplicationOperations.__INITIALIZATION_LOCK:
            if not AfeApplicationOperations.APPLICATION_INITIALIZED:
                cls._on_init()
                AfeApplicationOperations.APPLICATION_INITIALIZED = True

    @classmethod
    def _on_init(cls):
        cls._initialize_fl()
        cls.register_types()
        AfeStaticObjects.set_defaults()

    @classmethod
    def _initialize_fl(cls):
        FlInitializer.application_initialize()

    @classmethod
    def finalize_app(cls):
        """Finalizes application."""

    @classmethod
    def register_types(cls):
        """
        Registers ioc items
        :return: nothing
        """
