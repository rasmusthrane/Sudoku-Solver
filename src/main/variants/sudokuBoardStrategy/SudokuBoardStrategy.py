import abc

class SudokuBoardStrategy(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def getGridRepresentation(self) -> str:
        pass
    @abc.abstractmethod
    def getCols(self) -> str:
        pass
    @abc.abstractmethod
    def getRows(self) -> str:
        pass