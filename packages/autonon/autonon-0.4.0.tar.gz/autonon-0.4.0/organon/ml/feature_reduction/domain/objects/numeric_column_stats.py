"""Includes NumericColumnStats class"""


class NumericColumnStats:
    """Numeric Column Stats"""

    def __init__(self, column_name: str, mean: float, std: float, percentile_25: float, percentile_50: float,
                 percentile_75: float):
        self.column_name = column_name
        self.mean = mean
        self.std = std
        self.percentile_25 = percentile_25
        self.percentile_50 = percentile_50
        self.percentile_75 = percentile_75

    def __eq__(self, other):
        if not isinstance(other, NumericColumnStats):
            return NotImplemented

        return self.mean == other.mean and self.std == other.std and self.percentile_25 == other.percentile_25 \
               and self.percentile_50 == other.percentile_50 and self.percentile_75 == other.percentile_75
