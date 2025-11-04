from main.variants.strategy.sudoku_board import SudokuBoardStrategy
import abc

class GameFactory(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create_sudoku_board_strategy(self) -> SudokuBoardStrategy:
        pass