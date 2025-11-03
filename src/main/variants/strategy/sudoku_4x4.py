from main.variants.strategy.sudoku_board import SudokuBoardStrategy
from main.framework.utility import generate_sudoku_units

from typing import List, override

class Sudoku4by4(SudokuBoardStrategy):
    def __init__(self, clues:str) -> None:
        self._clues = clues
        self._cols: str = "1234"
        self._rows: str = "ABCD"
        self._nsubgrids: int = 4
        self._unitlist: List[List[str]] = generate_sudoku_units(self._rows, self._cols, self._nsubgrids)
        self._possible_digits: List[str] = ['1', '2', '3', '4']

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
    def unitlist(self) -> List[List[str]]:
        return self._unitlist
    
    @property
    @override
    def possible_digits(self) -> List[str]:
        return self._possible_digits