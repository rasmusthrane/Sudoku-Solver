from main.variants.strategy.sudoku_board import SudokuBoardStrategy
from main.framework.utility import generate_sudoku_units

from typing import List

class Sudoku4by4(SudokuBoardStrategy):
    def __init__(self, clues:str) -> None:
        self.clues = clues

    def getGridRepresentation(self) -> str:
        return self.clues

    def getCols(self) -> str:
        return "1234"
    
    def getRows(self) -> str:
        return "ABCD"
    
    def getNumberOfSubGrids(self) -> int:
        return 4
    
    def getUnitList(self) -> List[List[str]]:
        rows: str = self.getRows()
        cols: str = self.getCols()
        n_subgrids: int = self.getNumberOfSubGrids()
        unitlist: List[List[str]] = generate_sudoku_units(rows, cols, n_subgrids)

        return unitlist
    
    def getPossibleDigits(self) -> List[str]:
        return ['1', '2', '3', '4']