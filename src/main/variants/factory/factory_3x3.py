from main.variants.factory.game_factory import GameFactory
from main.variants.strategy.sudoku_board import SudokuBoardStrategy
from main.variants.strategy.sudoku_3x3 import Sudoku3by3

class Factory3x3(GameFactory):
    def __init__(self, clues:str = '.........') -> None:
        self.clues = clues

    def createSudokuBoardStrategy(self) -> SudokuBoardStrategy:
        return Sudoku3by3(self.clues)
    
