from main.framework.status import Status
from main.framework.GameState import GameState

import abc
from typing import Tuple, Dict, List

class FormalGameInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def getGameState(self) -> GameState:
        """
        Determine and return the current game state.

        Returns
        ---
            Either
                - "won": if all cells are filled and all Sudoku constraints are satisfied.

                - "ongoing": if the board is not yet complete and no constraints are violated.

                - "constraint_violation": if a Sudoku rule is broken (e.g. duplicate digits in a row, column, or block).
        """
        pass

    @abc.abstractmethod
    def getSudokuDimension(self) -> Tuple[int, int, int]:
        """
        Return the dimensions of the Sudoku grid.

        Returns
        ---
            Tuple[int, int, int]: A tuple containing:
                - number of rows in the grid
                - number of columns in the grid
                - number of subgrids (boxes) (e.g., 9 for a 9x9 Sudoku)
        """
        pass

    @abc.abstractmethod
    def getGridValueDict(self) -> Dict[str, str]:
        """
        Return the current values of the Sudoku grid.

        Returns
        ---
            Dict[str, str]: A dictionary containing:
                - key: cell
                - value: value
        """
        pass

    @abc.abstractmethod
    def getGridValues(self) -> List[str]:
        pass

    @abc.abstractmethod
    def getGridCandidateDict(self) -> Dict[str, str]:
        pass

    @abc.abstractmethod
    def getGridCandidateValues(self) -> List[str]:
        pass

    @abc.abstractmethod
    def getUnits(self) -> Dict[str, List[List[str]]]:
        pass

    @abc.abstractmethod
    def setCellValue(self, cell:str, value:str) -> Status:
        pass

    @abc.abstractmethod
    def removeCellValue(self, cell: str) -> Status:
        pass

