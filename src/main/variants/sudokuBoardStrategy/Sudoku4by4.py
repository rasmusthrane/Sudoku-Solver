from main.variants.sudokuBoardStrategy.SudokuBoardStrategy import SudokuBoardStrategy

from typing import List

#class Sudoku3by3(SudokuBoardStrategy):
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

        row_units = [[r + c for c in cols] for r in rows]
        col_units = [[r + c for r in rows] for c in cols]

        row_groups = [rows[i:i+2] for i in range(0, 4, 2)]
        col_groups = [cols[i:i+2] for i in range(0, 4, 2)]
        box_units = [[r + c for r in rg for c in cg] for rg in row_groups for cg in col_groups]

        unitlist = row_units + col_units + box_units
        return unitlist
    
    def getPossibleDigits(self) -> List[str]:
        return ['1', '2', '3', '4']