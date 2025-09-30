from main.framework.game import FormalGameInterface
from main.framework.status import Status
from main.framework.utility import cross
from main.variants.factory.GameFactory import GameFactory
from main.variants.factory.Factory3by3 import Factory3by3
from main.standard.GameConstants import GameConstants

from typing import Tuple, List, Dict, Set, override
from typing_extensions import Literal

class SquareSudokuGame(FormalGameInterface):
    def __init__(self, gameFactory: GameFactory) -> None:
        sudokuBoardStrategy = gameFactory.createSudokuBoardStrategy()
        self.cols = sudokuBoardStrategy.getCols()
        self.rows = sudokuBoardStrategy.getRows()
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
    
        self.nrows = len(self.rows)
        self.ncols = len(self.cols)
        self.nsubgrids = 1 
        self.ncells = len(self.cells)

        # Initialize grid representation
        self.initial_grid = sudokuBoardStrategy.getGridRepresentation()

        # Initialize grid value dict
        self.grid_value_dict: Dict[str, str] = {}
        self._populate_initial_grid_value_dict()

        # Initialize grid_candidate_dict
        self.grid_candidate_dict: Dict[str, str] = {}
        self._update_grid_candidate_dict()

        # Create list of initial clues
        self.initial_clues: List[str] = self._get_cells_with_clues()


    def _populate_initial_grid_value_dict(self):
        """
        Private method for populating grid_value_dict based on initial grid.
        """
        for i, c in enumerate(self.cells):
            value = self.initial_grid[i]
            self.grid_value_dict[c] = value
    
    def _update_grid_candidate_dict(self):
        for cell, value in self.grid_value_dict.items():
            if value != '.':
                self.grid_candidate_dict[cell] = value
        
        pass

    def _get_cells_with_clues(self) -> List[str]:
        initial_clues: List[str] = []
        for cell, value in self.grid_value_dict.items():
            if value != '.':
                initial_clues.append(cell)
        return initial_clues

    @override
    def getWinStatus(self) -> Literal["win", "ongoing"]:
        return "win"
    @override
    def getSudokuDimension(self) -> Tuple[int, int, int]:
        return self.nrows, self.ncols, self.nsubgrids
    @override
    def getGridValueDict(self) -> Dict[str, str]:
        return self.grid_value_dict
    @override
    def getGridValues(self) -> List[str]:
        return list(self.grid_value_dict.values())
    @override
    def getGridCandidateDict(self) -> Dict[str, str]:
        return {"A1": '', "B1": ''}
    @override
    def setCellValue(self, cell:str, value:str) -> Status:
        if cell in self.initial_clues:
            return Status.CANNOT_OVERWRITE_CLUE
        if value not in GameConstants.VALID_CHARS:
            return Status.INVALID_CHAR
        
        self.grid_value_dict[cell] = value
        return Status.OK
    
    # def setSudoku(self, sudoku_rep_with_clues: str) -> Status:
    #     invalid_chars = find_invalid_characters(sudoku_rep_with_clues)
    #     if invalid_chars:
    #         return Status.INVALID_CHAR

    #     duplicates = find_duplicates(sudoku_rep_with_clues)
    #     if duplicates:
    #         return Status.DUPLICATE_CLUE
        
    #     length_of_injected_rep = len(sudoku_rep_with_clues)
    #     if length_of_injected_rep > self.ncells:
    #         return Status.TOO_MANY_CHARS
        
    #     if length_of_injected_rep < self.ncells:
    #         return Status.TOO_FEW_CHARS
    
    #     else:
    #         self.grid = sudoku_rep_with_clues
    #         self._update_grid_value_dict()

    #         return Status.OK

if __name__ == "__main__":
    clues = "1.......9"
    game = SquareSudokuGame(Factory3by3(clues))

