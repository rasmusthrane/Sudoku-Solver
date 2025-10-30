from main.variants.strategy.sudoku_board import SudokuBoardStrategy
from main.framework.utility import cross

from typing import List

class Sudoku3by3(SudokuBoardStrategy):
    def __init__(self, clues:str) -> None:
        self.clues = clues


    def _setSudokuClues(self, clues:str) -> None:
        pass

    def getGridRepresentation(self) -> str:
        return self.clues

    def getCols(self) -> str:
        return "123"
    
    def getRows(self) -> str:
        return "ABC"
    
    def getNumberOfSubGrids(self) -> int:
        return 1
    
    def getUnitList(self) -> List[List[str]]:
        rows: str = self.getRows()
        cols: str = self.getCols()
        return [cross(rows, cols)]
    
    def getPossibleDigits(self) -> List[str]:
        return ['1', '2', '3', '4', '5', '6', '7', '8', '9']