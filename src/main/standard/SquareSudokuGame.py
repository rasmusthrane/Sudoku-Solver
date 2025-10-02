from main.framework.game import FormalGameInterface
from main.framework.status import Status
from main.framework.utility import cross
from main.variants.factory.GameFactory import GameFactory
from main.variants.factory.Factory3by3 import Factory3by3
from main.standard.GameConstants import GameConstants
from main.framework.GameState import GameState

from typing import Tuple, List, Dict, override
import sys #type:ignore

class SquareSudokuGame(FormalGameInterface):
    def __init__(self, gameFactory: GameFactory) -> None:
        sudokuBoardStrategy = gameFactory.createSudokuBoardStrategy()
        self.cols = sudokuBoardStrategy.getCols()
        self.rows = sudokuBoardStrategy.getRows()
        self.cells = cross(self.rows, self.cols)
        self.unitlist = ([cross(self.rows, self.cols)]) # Only one unit in small sudoku 

        # Create a dict that holds all units that each cell belongs to
        self.units = self.__create_unit_dict()
        # Create a dict that holds all cells which shares unit with a cell
        self.peers = self.__create_peers_dict()
        
        self.nrows = len(self.rows)
        self.ncols = len(self.cols)
        self.nsubgrids = 1 
        self.ncells = len(self.cells)

        # Initialize grid representation
        self.initial_grid = sudokuBoardStrategy.getGridRepresentation()

        # Initialize grid value dict
        self.grid_value_dict: Dict[str, str] = {}
        self.__populate_initial_grid_value_dict()

        # Initialize grid_candidate_dict
        self.grid_candidate_dict: Dict[str, str] = {}
        self.__update_grid_candidate_dict()

        # Create list of initial clues
        self.initial_clues: List[str] = self.__get_cells_with_clues()

        self.game_state: GameState = 'ongoing'
        self.__update_game_state()

    def __create_peers_dict(self) -> Dict[str, List[str]]:
        peers: Dict[str, List[str]] = {}
        for c in self.cells:
            all_cells: List[str] = [] # Flattened list to hold all cells that share unit with s
            for unit in self.units[c]:
                all_cells.extend(unit)
            peers_of_c: List[str] = sorted(list(set(all_cells) - set([c])))
            peers[c] = peers_of_c
        return peers

    def __create_unit_dict(self) -> Dict[str, List[List[str]]]:
        units: Dict[str, List[List[str]]] = {}
        for c in self.cells:
            units_for_s: List[List[str]] = []  # List to hold units containing s
            for u in self.unitlist:
                if c in u:
                    units_for_s.append(u)
            units[c] = units_for_s
        return units

    def __populate_initial_grid_value_dict(self) -> None:
        for i, c in enumerate(self.cells):
            value = self.initial_grid[i]
            self.grid_value_dict[c] = value
    
    def __update_grid_candidate_dict(self) -> None:
        for cell, value in self.grid_value_dict.items():

            # First check if a digit is placed
            digit_placed: bool = value != '.'
            if digit_placed:
                list_of_candidates = list(value) # the only candidate is the value itself

            # Then elimate all possible candidates
            else:
                list_of_candidates = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
                for peer_of_cell in self.peers[cell]:
                    peer_value_is_candidate: bool = self.grid_value_dict[peer_of_cell] in list_of_candidates
                    if peer_value_is_candidate:
                        list_of_candidates.remove(self.grid_value_dict[peer_of_cell])

            # create string to represent candidates
            self.grid_candidate_dict[cell] = "".join(str(candidate) for candidate in list_of_candidates)               

    def __get_cells_with_clues(self) -> List[str]:
        initial_clues: List[str] = []
        for cell, value in self.grid_value_dict.items():
            if value != '.':
                initial_clues.append(cell)
        return initial_clues

    def __update_game_state(self) -> None:
        unique_solution_found: bool = list(self.grid_candidate_dict.values()) == list(self.grid_value_dict.values())
        if unique_solution_found:
            self.game_state: GameState = 'won'

    @override
    def getGameState(self) -> GameState:
        return self.game_state
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
    clues = "12345678."
    game = SquareSudokuGame(Factory3by3(clues))

