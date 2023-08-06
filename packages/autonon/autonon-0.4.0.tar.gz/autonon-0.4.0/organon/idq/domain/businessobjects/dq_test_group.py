"""todo"""
from organon.idq.domain.enums.dq_test_group_type import DqTestGroupType


class DqTestGroup:
    """todo"""

    def __init__(self):
        self.group_type: DqTestGroupType = None
        self.min_bmh: int = None
        self.test_bmh: int = None
        self.inclusion_flag: bool = None
