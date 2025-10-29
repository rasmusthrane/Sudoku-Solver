from main.variants.strategy.sudoku_board import SudokuBoardStrategy
from main.framework.utility import generate_sudoku_units

from typing import List, override


class Sudoku9x9(SudokuBoardStrategy):
    def __init__(self, clues: str) -> None:
        self.clues = clues
    
    @override
    def getGridRepresentation(self) -> str:
        return self.clues

    @override
    def getCols(self) -> str:
        return 'ABCDEFGHI'

    @override
    def getRows(self) -> str:
        return '123456789'
    
    @override
    def getNumberOfSubGrids(self) -> int:
        return 9
    
    @override
    def getPossibleDigits(self) -> List[str]:
        return ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    
    @override
    def getUnitList(self) -> List[List[str]]:
        rows: str = self.getRows()
        cols: str = self.getCols()
        n_subgrids: int = self.getNumberOfSubGrids()
        unitlist: List[List[str]] = generate_sudoku_units(rows, cols, n_subgrids)
        return unitlist
