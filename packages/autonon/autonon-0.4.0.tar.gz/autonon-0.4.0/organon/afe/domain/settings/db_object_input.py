"""
This module include DbObjectInput class.
"""
from organon.afe.domain.common.reader_helper import get_values_from_kwargs

DbObjClass = object
try:
    from organon.fl.dataaccess.datadtos.db_object_dto import DbObjectDto

    DbObjClass = DbObjectDto  # pycharm warninglerin kaldırılması için böyle yapıldı
except ImportError:
    pass


class DbObjectInput(DbObjClass):  # pylint: disable=useless-object-inheritance
    """Db Object with connection name specified"""

    ATTR_DICT = {
        "schema_name": str,
        "table_name": str,
        "sql_statement": str,
        "connection_name": str
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connection_name = None

        get_values_from_kwargs(self, self.ATTR_DICT, kwargs)
