"""This module includes DataFrameOperationsFactory class."""
from organon.fl.core.businessobjects.dask_dataframe import DaskDataFrame
from organon.fl.core.businessobjects.dataframe import DataFrame
from organon.fl.core.businessobjects.dict_dataframe import DictDataFrame
from organon.fl.core.businessobjects.idataframe import IDataFrame
from organon.fl.mathematics.helpers.dask_dataframe_operations import DaskDataFrameOperations
from organon.fl.mathematics.helpers.dict_dataframe_operations import DictDataFrameOperations
from organon.fl.mathematics.helpers.pandas_dataframe_operations import PandasDataFrameOperations


class DataFrameOperationsFactory:
    """Class for DataFrameOperationsFactory"""

    @staticmethod
    def get_dataframe_operations(df_obj: IDataFrame):
        """ check whether we have dask or not and return dask operations accordingly"""
        if isinstance(df_obj, DictDataFrame):
            return DictDataFrameOperations()
        if isinstance(df_obj, DataFrame):
            return PandasDataFrameOperations()
        if isinstance(df_obj, DaskDataFrame):
            return DaskDataFrameOperations()
        raise NotImplementedError
