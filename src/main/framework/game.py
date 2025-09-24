from main.framework.status import Status

import abc
from typing_extensions import Literal
from typing import Tuple, Dict

class FormalGameInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def getWinStatus(self) -> Literal["win", "ongoing"]:
        """Return the current win status of the game."""
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
    def setSudoku(self, sudoku_rep_with_clues: str) -> Status:
        """
        Inject clues into an empty Sudoku by m  odifying the grid.
        Returns the status of the mutator call

        """
        pass
