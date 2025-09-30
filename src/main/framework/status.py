from enum import Enum, auto

class Status(Enum):
    OK = auto()
    CANNOT_OVERWRITE_CLUE = auto()
    # DUPLICATE_CLUE = auto()
    # INVALID_CHAR = auto()
    # TOO_MANY_CHARS = auto()
    # TOO_FEW_CHARS = auto()