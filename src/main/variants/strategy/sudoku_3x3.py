from main.variants.strategy.sudoku_board import SudokuBoardStrategy
from main.framework.utility import cross

from typing import List, override

class Sudoku3by3(SudokuBoardStrategy):
    def __init__(self, clues:str) -> None:
        self._clues = clues
        self._cols: str = "123"
        self._rows: str = "ABC"
        self._nsubgrids: int = 1
        self._all_units: List[List[str]] = [cross(self._rows, self._cols)]
        self._possible_digits: List[str] = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    @property
    @override
    def initial_grid(self) -> str:
        return self._clues

    @property
    @override
    def cols(self) -> str:
        return self._cols 
    
    @property
    @override
    def rows(self) -> str:
        return self._rows
    
    @property
    @override
    def nsubgrids(self) -> int:
        return self._nsubgrids
    
    @property
    @override
    def all_units(self) -> List[List[str]]:
        return self._all_units
    
    @property
    @override
    def possible_digits(self) -> List[str]:
        return self._possible_digits