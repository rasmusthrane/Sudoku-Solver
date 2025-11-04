from main.variants.factory.game_factory import GameFactory
from main.variants.strategy.sudoku_board import SudokuBoardStrategy
from main.variants.strategy.sudoku_4x4 import Sudoku4by4

class Factory4x4(GameFactory):
    def __init__(self, clues:str = '................') -> None:
        self.clues = clues

    def create_sudoku_board_strategy(self) -> SudokuBoardStrategy:
        return Sudoku4by4(self.clues)
    
