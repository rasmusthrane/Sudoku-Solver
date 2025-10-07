from enum import Enum, auto

class Status(Enum):
    OK = auto()
    CANNOT_OVERWRITE_CLUE = auto()
    INVALID_CHAR = auto()
    CELL_DOES_NOT_EXIST = auto()
    INVALID_DIGIT = auto()
    # DUPLICATE_CLUE = auto()
    # TOO_MANY_CHARS = auto()
    # TOO_FEW_CHARS = auto()