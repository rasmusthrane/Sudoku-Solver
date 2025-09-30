from main.variants.sudokuBoardStrategy.SudokuBoardStrategy import SudokuBoardStrategy
from main.framework.utility import find_duplicates, find_invalid_characters

class Sudoku3by3(SudokuBoardStrategy):
    def __init__(self, clues:str) -> None:
        if len(clues) != 9:
            raise ValueError(f"Expected 9 characters, got {len(clues)}")

        invalid_chars = find_invalid_characters(clues)
        if invalid_chars:
            raise ValueError(f"Invalid characters in clues: {invalid_chars}")

        duplicates = find_duplicates(clues)
        if duplicates:
            raise ValueError(f"Duplicate values found in clues: {duplicates}")

        self.clues = clues


    def _setSudokuClues(self, clues:str) -> None:
        pass

    def getGridRepresentation(self) -> str:
        return self.clues

    def getCols(self) -> str:
        return "123"
    
    def getRows(self) -> str:
        return "ABC"