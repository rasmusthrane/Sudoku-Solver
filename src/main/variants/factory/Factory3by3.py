from main.variants.factory.GameFactory import GameFactory
from main.variants.sudokuBoardStrategy.sudoku_board_strategy import SudokuBoardStrategy
from main.variants.sudokuBoardStrategy.sudoku_3x3 import Sudoku3by3

class Factory3by3(GameFactory):
    def __init__(self, clues:str = '.........') -> None:
        self.clues = clues

    def createSudokuBoardStrategy(self) -> SudokuBoardStrategy:
        return Sudoku3by3(self.clues)
    
