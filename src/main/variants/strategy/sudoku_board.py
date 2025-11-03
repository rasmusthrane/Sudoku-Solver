import abc
from typing import List

class SudokuBoardStrategy(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def initial_grid(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def cols(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def rows(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def nsubgrids(self) -> int:
        pass
    
    @property
    @abc.abstractmethod
    def unitlist(self) -> List[List[str]]:
        pass

    @property
    @abc.abstractmethod
    def possible_digits(self) -> List[str]:
        pass