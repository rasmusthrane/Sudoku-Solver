from main.variants.strategy.sudoku_board import SudokuBoardStrategy
import abc

class GameFactory(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def createSudokuBoardStrategy(self) -> SudokuBoardStrategy:
        pass