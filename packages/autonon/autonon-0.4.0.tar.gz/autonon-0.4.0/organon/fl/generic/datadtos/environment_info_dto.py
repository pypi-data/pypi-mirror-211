"""
This class keeps the EnvironmentInfoDto class.
"""


class EnvironmentInfoDto:
    """
    This class keeps the environment info.
    """
    def __init__(self, machine_name: str, user_name: str):
        self.machine_name = machine_name
        self.user_name = user_name
