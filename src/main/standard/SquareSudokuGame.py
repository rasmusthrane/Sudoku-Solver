from main.framework.game import FormalGameInterface
from main.framework.utility import cross, find_duplicates, find_invalid_characters
from main.standard.GameConstants import GameConstants
from main.framework.status import Status

from typing import Tuple, List, Dict, Set
from typing_extensions import Literal

class SquareSudokuGame(FormalGameInterface):
    def __init__(self) -> None:
        self.cols = "123"
        self.rows = "ABC"
        self.cells = cross(self.rows, self.cols)
        self.unitlist = ([cross(self.rows, self.cols)]) # Only one unit in small sudoku 

        # Create a dict that holds all units that each cell belongs to
        self.units: Dict[str, List[List[str]]] = {}
        for c in self.cells:
            units_for_s: List[List[str]] = []  # List to hold units containing s
            for u in self.unitlist:
                if c in u:
                    units_for_s.append(u)
            self.units[c] = units_for_s
        # Create a dict that holds all cells which shares unit with a cell
        self.peers: Dict[str, Set[str]] = {}
        for c in self.cells:
            all_cells: List[str] = [] # Flattened list to hold all cells that share unit with s
            for unit in self.units[c]:
                all_cells.extend(unit)
            peers_of_c: Set[str] = set(all_cells) - set([c])
            self.peers[c] = peers_of_c
        print(self.peers)
        self.nrows = len(self.rows)
        self.ncols = len(self.cols)
        self.nsubgrids = 1 
        self.ncells = len(self.cells)

        # Initialize grid representation
        self.grid = GameConstants.EMPTY_CELL*self.ncells

        # Initialize grid value dict
        self.grid_value_dict: Dict[str, str] = {}
        self._update_grid_value_dict()

        # Initialize grid_candidate_dict
        self.grid_candidate_dict: Dict[str, str] = {}
        self._update_grid_candidate_dict()

    def _update_grid_value_dict(self):
        """
        Private method for updating the values of the grid_value_dict based on self.grid.
        """
        for i, c in enumerate(self.cells):
            value = self.grid[i]
            self.grid_value_dict[c] = value
    
    def _update_grid_candidate_dict(self):
        for cell, value in self.grid_value_dict.items():
            if value != '.':
                self.grid_candidate_dict[cell] = value
        
        print(self.grid_candidate_dict)
        pass

    def getWinStatus(self) -> Literal["win", "ongoing"]:
        return "win"
    
    def getSudokuDimension(self) -> Tuple[int, int, int]:
        return self.nrows, self.ncols, self.nsubgrids
    
    def getGridValueDict(self) -> Dict[str, str]:
        return self.grid_value_dict
    
    def getGridCandidateDict(self) -> Dict[str, str]:
        return {"A1": '', "B1": ''}
    
    def setSudoku(self, sudoku_rep_with_clues: str) -> Status:
        invalid_chars = find_invalid_characters(sudoku_rep_with_clues)
        if invalid_chars:
            return Status.INVALID_CHAR

        duplicates = find_duplicates(sudoku_rep_with_clues)
        if duplicates:
            return Status.DUPLICATE_CLUE
        
        length_of_injected_rep = len(sudoku_rep_with_clues)
        if length_of_injected_rep > self.ncells:
            return Status.TOO_MANY_CHARS
        
        if length_of_injected_rep < self.ncells:
            return Status.TOO_FEW_CHARS
    
        else:
            self.grid = sudoku_rep_with_clues
            self._update_grid_value_dict()

            return Status.OK

if __name__ == "__main__":
    game = SquareSudokuGame()
    clues = "1........"
    game.setSudoku(clues)
    # game._update_grid_candidate_dict()

