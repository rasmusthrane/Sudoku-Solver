from main.framework.status import Status
from main.framework.gamestate import GameState

import abc
from typing import Tuple, Dict, List

class FormalGameInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def compute_violating_cells(self) -> List[str]:
        """
        Compute the cells that currently violate a constraint. If none are found, return an empty list.
        """
        pass
    
    @property
    @abc.abstractmethod
    def game_state(self) -> GameState:
        """
        Return the current game state.

        Returns
        ---
            Either
                - "won": if all cells are filled and all Sudoku constraints are satisfied.

                - "ongoing": if the board is not yet complete and no constraints are violated.

                - "constraint_violation": if a Sudoku rule is broken (e.g. duplicate digits in a row, column, or block).
        """
        pass
    
    @property
    @abc.abstractmethod
    def sudoku_dims(self) -> Tuple[int, int, int]:
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

    @property
    @abc.abstractmethod
    def value_dict(self) -> Dict[str, str]:
        """
        Return the current values of the Sudoku grid.

        Returns
        ---
            Dict[str, str]: A dictionary containing:
                - key: cell
                - value: value
        """
        pass

    @property    
    @abc.abstractmethod
    def grid_values(self) -> List[str]:
        pass

    @property
    @abc.abstractmethod
    def candidate_dict(self) -> Dict[str, str]:
        pass

    @property
    @abc.abstractmethod
    def candidate_values(self) -> List[str]:
        pass
    
    @property
    @abc.abstractmethod
    def units(self) -> Dict[str, List[List[str]]]:
        """
        A mapping of each cell to the list of all units it belongs to.

        A *unit* is a collection of cells that share a constraint,
        such as a row, a column, or a 3x3 box.
        """
        pass

    @property
    @abc.abstractmethod
    def peers(self) -> Dict[str, List[str]]:
        """
        A mapping of each cell to all other cells that share a unit with it.

        *Peers* of a cell are all distinct cells that appear in the same row, column, or box.
        """
        pass

    @property
    @abc.abstractmethod
    def n_empty_cells(self) -> int:
        pass
    
    @abc.abstractmethod
    def value_of(self, cell: str) -> str:
        pass

    @abc.abstractmethod
    def peers_of(self, cell: str) -> List[str]:
        pass

    @abc.abstractmethod
    def set_cell_value(self, cell:str, value:str) -> Status:
        pass

    @abc.abstractmethod
    def remove_cell_value(self, cell: str) -> Status:
        pass

    @abc.abstractmethod
    def solve_sudoku(self) -> None:
        pass

