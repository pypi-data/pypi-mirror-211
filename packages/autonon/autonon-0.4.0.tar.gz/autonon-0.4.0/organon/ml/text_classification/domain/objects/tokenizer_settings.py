"""settings class for word tokenization"""


class TokenizerSettings:
    """word tokenization parameters class"""

    def __init__(self, padding: str = "max_length", truncation: bool = True, max_length: int = 128):
        self.padding: str = padding
        self.truncation: bool = truncation
        self.max_length: int = max_length
