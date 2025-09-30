from enum import Enum, auto

class Status(Enum):
    OK = auto()
    CANNOT_OVERWRITE_CLUE = auto()
    INVALID_CHAR = auto()
    # DUPLICATE_CLUE = auto()
    # TOO_MANY_CHARS = auto()
    # TOO_FEW_CHARS = auto()