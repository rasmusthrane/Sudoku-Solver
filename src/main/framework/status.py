from enum import Enum, auto

class Status(Enum):
    OK = auto()
    DUPLICATE_CLUE = auto()
    INVALID_CHAR = auto()