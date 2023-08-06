"""Includes UserDbObjLocator class."""


class UserDbObjLocator:
    """Class for db object location definition in user input"""

    def __init__(self):
        self.connection_name: str = None
        self.table_name: str = None
        self.schema_name: str = None
        self.sql_statement: str = None
