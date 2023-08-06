"""
This module keeps the function used in ioc operations.
"""
from typing import Dict, TypeVar, Type

from organon.fl.core.exceptionhandling.known_exception import KnownException
from .ioc_registration_item import IocRegistrationItem
from ..businessobjects.fl_core_static_objects import FlCoreStaticObjects

IocAbstractType = TypeVar("IocAbstractType")


def register_type(item: IocRegistrationItem):
    """
    Checks if the item is already registered or not
    If so, raises a KnownException
    If not, registers the item
    :param item: IocRegistrationItem
    :return: nothing
    """
    if FlCoreStaticObjects.ioc_registered_items is None:
        FlCoreStaticObjects.ioc_registered_items = []

    for ioc_registered_item in FlCoreStaticObjects.ioc_registered_items:  # pylint: disable=not-an-iterable
        abstract_type_name = ioc_registered_item.abstract_type.__name__

        if ioc_registered_item.ioc_key == item.ioc_key and abstract_type_name == item.abstract_type.__name__:
            raise KnownException("Ioc key : " + ioc_registered_item.ioc_key + " abstract type : " + abstract_type_name +
                                 " is already registered")

    FlCoreStaticObjects.ioc_registered_items.append(item)


def resolve(abstract_type: Type[IocAbstractType], ioc_key: str, init_args: Dict = None, no_initialize=False, ) \
        -> IocAbstractType:
    """
    Resolves and returns the concrete type of the ioc registered item according to its abstract type and ioc key
    :param abstract_type: abstract type of the item
    :param ioc_key: ioc key of the item
    :param init_args: Creates an instance of concrete type with given arguments
    :param no_initialize: If true, does not create an instance and just returns concrete type
    :return: concrete type of the item
    """
    if FlCoreStaticObjects.ioc_registered_items is None:
        raise KnownException("No types registered")

    for ioc_registered_item in FlCoreStaticObjects.ioc_registered_items:  # pylint: disable=not-an-iterable
        abstract_type_name = ioc_registered_item.abstract_type.__name__

        if (ioc_registered_item.ioc_key == ioc_key) & (abstract_type_name == abstract_type.__name__):
            if not no_initialize:
                if init_args:
                    return ioc_registered_item.concrete_type(**init_args)
                return ioc_registered_item.concrete_type()
            return ioc_registered_item.concrete_type
    return None
