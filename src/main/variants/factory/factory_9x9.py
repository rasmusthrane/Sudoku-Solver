from main.variants.factory.game_factory import GameFactory
from main.variants.strategy.sudoku_board import SudokuBoardStrategy
from main.variants.strategy.sudoku_9x9 import Sudoku9x9

class Factory9x9(GameFactory):
    def __init__(self, clues:str= \
                 '......... \
                  ......... \
                  ......... \
                  ......... \
                  ......... \
                  ......... \
                  ......... \
                  ......... \
                  .........') -> None:
        self.clues = clues

    def createSudokuBoardStrategy(self) -> SudokuBoardStrategy:
        return Sudoku9x9(self.clues)
    
