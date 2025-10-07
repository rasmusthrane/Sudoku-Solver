from main.variants.sudokuBoardStrategy.SudokuBoardStrategy import SudokuBoardStrategy

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