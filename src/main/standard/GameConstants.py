from typing import Set, Literal

GameState = Literal['won', 'ongoing', 'constraint_violation']

class GameConstants:
    EMPTY_CELL: str = '.'
    VALID_CHARS: Set[str] = {EMPTY_CELL, '1', '2', '3', '4', '5', '6', '7', '8', '9'}