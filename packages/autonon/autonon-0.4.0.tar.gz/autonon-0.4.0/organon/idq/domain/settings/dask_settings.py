"""Includes Class for Dask Settings"""


class DaskSettings:
    """Class for Dask Settings"""

    def __init__(self):
        self.client = None
        self.use_dask: bool = True
        self.submit_args: dict = None
