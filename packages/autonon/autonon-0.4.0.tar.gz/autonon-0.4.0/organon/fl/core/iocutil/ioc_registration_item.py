"""
This module keeps the IocRegistrationItem class.
"""


class IocRegistrationItem:
    """
    Holds the features such as ioc key, abstract type and concrete type to be used in IoC
    """
    def __init__(self, ioc_key: str, abstract_type: type, concrete_type: type):
        self.ioc_key = ioc_key
        self.abstract_type = abstract_type
        self.concrete_type = concrete_type
