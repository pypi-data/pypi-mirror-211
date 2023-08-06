"""
This module includes BinaryTarget class.
"""
from organon.afe.domain.common.reader_helper import get_values_from_kwargs


class BinaryTarget:
    """
    Information for AFE target columns of 'Binary' type
    """

    ATTR_DICT = {
        "positive_category": str,
        "negative_category": str,
        "indeterminate_category": str,
        "exclusion_category": str
    }

    def __init__(self, **kwargs):
        self.positive_category: str = None
        self.negative_category: str = None
        self.indeterminate_category: str = None
        self.exclusion_category: str = None

        get_values_from_kwargs(self, self.ATTR_DICT, kwargs)

    def __deepcopy__(self, memo):
        output = BinaryTarget()
        output.positive_category = self.positive_category
        output.negative_category = self.negative_category
        output.indeterminate_category = self.indeterminate_category
        output.exclusion_category = self.exclusion_category
        return output
