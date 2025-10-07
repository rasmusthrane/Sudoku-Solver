import abc
from typing import List

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
    @abc.abstractmethod
    def getNumberOfSubGrids(self) -> int:
        pass
    @abc.abstractmethod
    def getUnitList(self) -> List[List[str]]:
        pass