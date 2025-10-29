from main.variants.factory.GameFactory import GameFactory
from main.variants.sudokuBoardStrategy.sudoku_board_strategy import SudokuBoardStrategy
from main.variants.sudokuBoardStrategy.sudoku_4x4 import Sudoku4by4

class Factory4by4(GameFactory):
    def __init__(self, clues:str = '................') -> None:
        self.clues = clues

    def createSudokuBoardStrategy(self) -> SudokuBoardStrategy:
        return Sudoku4by4(self.clues)
    
