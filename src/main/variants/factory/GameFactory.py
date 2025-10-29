from main.variants.sudokuBoardStrategy.sudoku_board_strategy import SudokuBoardStrategy
import abc

class GameFactory(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def createSudokuBoardStrategy(self) -> SudokuBoardStrategy:
        pass