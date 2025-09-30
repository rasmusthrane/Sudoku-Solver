from main.variants.sudokuBoardStrategy.SudokuBoardStrategy import SudokuBoardStrategy
import abc

class GameFactory(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def createSudokuBoardStrategy(self) -> SudokuBoardStrategy:
        pass