from main.framework.game import FormalGameInterface
from main.framework.status import Status
from main.framework.utility import cross, find_invalid_characters
from main.variants.factory.game_factory import GameFactory
from main.standard.game_constants import GameConstants
from main.framework.gamestate import GameState

from typing import Tuple, List, Dict, override
from collections import defaultdict
import sys #type:ignore

class SquareSudokuGame(FormalGameInterface):
    def __init__(self, game_factory: GameFactory) -> None:
        sudoku_board_strategy = game_factory.create_sudoku_board_strategy()
        self.cols: str = sudoku_board_strategy.cols
        self.rows: str = sudoku_board_strategy.rows
        self.cells: List[str] = cross(self.rows, self.cols)
        self.all_units: List[List[str]] = sudoku_board_strategy.all_units
        self.possible_digits: List[str] = sudoku_board_strategy.possible_digits
        self.nrows: int = len(self.rows)
        self.ncols: int = len(self.cols)
        self.nsubgrids: int = sudoku_board_strategy.nsubgrids
        self.ncells: int = len(self.cells)

        # Create a dict that holds all units that each cell belongs to
        self._units: Dict[str, List[List[str]]] = self._create_unit_dict()
        # Create a dict that holds all cells which shares unit with a cell
        self._peers: Dict[str, List[str]] = self._create_peers_dict()

        # Initialize grid representation
        self.initial_grid: str = sudoku_board_strategy.initial_grid

        # Check if initial injected grid has a valid length
        self._validate_initial_grid_length()
        
        # Initialize grid value dict
        self._value_dict: Dict[str, str] = self._create_initial_value_dict()
        
        # Check if initial injected grid uses valid characters
        self._validate_characters_in_initial_grid()

        # Check if initial injected grid violates any constraints
        self._validate_if_any_constraints_are_violated()
            
        # Initialize grid_candidate_dict
        self._candidate_dict: Dict[str, str] = {}
        self._update_candidate_dict()

        # Create list of initial clues
        self.initial_clues: List[str] = self._get_cells_with_clues()

        # Set the game state to 'ongoing' and check if any updates have happened
        self._game_state: GameState = 'ongoing'
        self._update_game_state()

    def _validate_if_any_constraints_are_violated(self):
        if self._is_constraint_violated():
            violating_cells = self.compute_violating_cells()
            raise ValueError(f"Initial clues violate a constraint. Violating cells are {violating_cells}")

    def _validate_characters_in_initial_grid(self):
        invalid_chars = find_invalid_characters(self.initial_grid)
        if invalid_chars:
            raise ValueError(f"Invalid characters in cells: {invalid_chars}")

    def _validate_initial_grid_length(self) -> None:
        expected_n_cells = len(self.cells)
        actual_n_cells = len(self.initial_grid)
        if actual_n_cells > expected_n_cells:
            raise ValueError(f"Too many cells. Expected {expected_n_cells} cells, got {actual_n_cells}")
        if actual_n_cells < expected_n_cells:
            raise ValueError(f"Too few cells. Expected {expected_n_cells} cells, got {actual_n_cells}")

    def _create_peers_dict(self) -> Dict[str, List[str]]:
        peers: Dict[str, List[str]] = {}
        for c in self.cells:
            all_cells: List[str] = [] # Flattened list to hold all cells that share unit with s
            for unit in self.units[c]:
                all_cells.extend(unit)
            peers_of_c: List[str] = sorted(list(set(all_cells) - set([c])))
            peers[c] = peers_of_c
        return peers

    def _create_unit_dict(self) -> Dict[str, List[List[str]]]:
        units: Dict[str, List[List[str]]] = {}
        for c in self.cells:
            units_for_s: List[List[str]] = []  # List to hold units containing s
            for u in self.all_units:
                if c in u:
                    units_for_s.append(u)
            units[c] = units_for_s
        return units

    def _create_initial_value_dict(self) -> Dict[str, str]:
        value_dict: Dict[str, str] = {}
        for i, c in enumerate(self.cells):
            value = self.initial_grid[i]
            value_dict[c] = value
        
        return value_dict
    
    def _update_candidate_dict(self) -> None:
        for cell, value in self._value_dict.items():

            # First check if a digit is placed
            digit_placed: bool = value != '.'
            if digit_placed:
                list_of_candidates = list(value) # the only candidate is the value itself

            # Then elimate all possible candidates
            else:
                list_of_candidates = self.possible_digits.copy()
                for peer in self.peers_of(cell):
                    peer_value_is_candidate: bool = self.value_of(peer) in list_of_candidates
                    if peer_value_is_candidate:
                        list_of_candidates.remove(self.value_of(peer))
                
            # create string to represent candidates
            self._candidate_dict[cell] = "".join(str(candidate) for candidate in list_of_candidates)           

    def _get_cells_with_clues(self) -> List[str]:
        initial_clues: List[str] = []
        for cell, value in self._value_dict.items():
            if value != '.':
                initial_clues.append(cell)
        return initial_clues
    
    def _check_if_cell_violates_constraint(self, cell:str) -> bool:
        cell_value = self.value_of(cell)
        if cell_value == GameConstants.EMPTY_CELL:
            return False

        return any(cell_value == self.value_of(peer) for peer in self.peers_of(cell))

    def _is_constraint_violated(self) -> bool:
        return any(self._check_if_cell_violates_constraint(cell) for cell in self.cells)

    def _update_game_state(self) -> None:
        if self._is_constraint_violated():
            self._game_state: GameState = 'constraint_violation'
            return
        
        unique_solution_found: bool = self.grid_values == self.candidate_values
        if unique_solution_found:
            self._game_state: GameState = 'won'
            return
        
        self._game_state: GameState = 'ongoing'
        
    @override
    def compute_violating_cells(self) -> List[str]:
        violating_cells: List[str] = []
        for cell, cell_value in self._value_dict.items():
            if cell_value == GameConstants.EMPTY_CELL: continue 
            for peer in self.peers_of(cell):
                peer_value = self.value_of(peer)
                if cell_value == peer_value:
                    violating_cells.append(cell)
                    break
        
        return violating_cells

    @property
    @override
    def game_state(self) -> GameState:
        return self._game_state
    
    @property
    @override
    def sudoku_dims(self) -> Tuple[int, int, int]:
        return self.nrows, self.ncols, self.nsubgrids
    
    @property
    @override
    def value_dict(self) -> Dict[str, str]:
        return self._value_dict
    
    @property
    @override
    def grid_values(self) -> List[str]:
        return list(self._value_dict.values())
    
    @property
    @override
    def candidate_dict(self) -> Dict[str, str]:
        return self._candidate_dict
    
    @property
    @override
    def candidate_values(self) -> List[str]:
        return list(self._candidate_dict.values())
    
    @property
    @override
    def units(self) -> Dict[str, List[List[str]]]:
        return self._units
    
    @property
    @override
    def peers(self) -> Dict[str, List[str]]:
        return self._peers

    @property
    @override
    def n_empty_cells(self) -> int:
        return len([cell for cell in self.cells if self.value_of(cell) == GameConstants.EMPTY_CELL])
    
    @override
    def value_of(self, cell: str) -> str:
        return self._value_dict[cell]
    
    @override
    def peers_of(self, cell: str) -> List[str]:
        return self._peers[cell]

    @override
    def set_cell_value(self, cell:str, value:str) -> Status:
        if cell in self.initial_clues:
            return Status.CANNOT_OVERWRITE_CLUE
        if cell not in self.cells:
            return Status.CELL_DOES_NOT_EXIST
        if value not in GameConstants.VALID_CHARS and not value.isnumeric():
            return Status.NOT_A_NUMBER
        if value not in self.possible_digits and value != GameConstants.EMPTY_CELL:
            return Status.INVALID_DIGIT
        
        self._value_dict[cell] = value
        self._update_candidate_dict()
        self._update_game_state()

        return Status.OK
    
    @override
    def remove_cell_value(self, cell: str) -> Status:
        status = self.set_cell_value(cell, GameConstants.EMPTY_CELL)
        return status
    
    @override
    def solve_sudoku(self) -> None:
        self._place_all_hidden_singles()        
        
    def _place_hidden_singles(self, unit: List[str]) -> None:
        """
        Finds and places hidden singles within a given Sudoku unit (row, column, or box).

        A hidden single is a digit that appears as a candidate in only one empty cell
        within the unit. This method scans all empty cells in the unit, identifies digits
        that are candidates in exactly one cell, and sets that digit in its corresponding cell.
        """
        digit_count: Dict[str, int] = defaultdict(int)
        last_cell_to_see_digit: Dict[str, str] = {}
        for cell in unit:
            cell_is_empty: bool = self.value_of(cell) == GameConstants.EMPTY_CELL
            if cell_is_empty:
                for digit in self.candidate_dict[cell]:
                    digit_count[digit] += 1
                    last_cell_to_see_digit[digit] = cell 
        
        hidden_singles = [digit for digit in digit_count.keys() if digit_count[digit] == 1]
        for hidden_single in hidden_singles:
            cell_to_place_in = last_cell_to_see_digit[hidden_single]
            self.set_cell_value(cell_to_place_in, hidden_single)
        

    def _place_all_hidden_singles(self) -> None:
        """
        Repeatedly places all hidden singles on the board. 
        This method continues to perform passes over the board until no new hidden singles can be placed, 
        i.e., the board reaches a stable state  with respect to hidden singles.
        """
        while True:
            empty_cells = [cell for cell in self.value_dict.keys() if self.value_of(cell) == GameConstants.EMPTY_CELL]
            n_empty_cells_before = self.n_empty_cells
            for cell in empty_cells:
                for unit in self.units[cell]:
                    self._place_hidden_singles(unit)

            n_empty_cells_after = self.n_empty_cells
            if n_empty_cells_before == n_empty_cells_after:
                break

    
if __name__ == "__main__":
    from main.variants.factory.factory_3x3 import Factory3x3 #type:ignore
    from main.variants.factory.factory_4x4 import Factory4x4 #type:ignore
    from main.variants.factory.factory_9x9 import Factory9x9 #type:ignore
    from testing.utility.TestHelper import TestHelper as th  #type:ignore

    row_A = ".2.6.8..."
    row_B = "58...97.."
    row_C = "....4...."
    row_D = "37....5.."
    row_E = "6.......4"
    row_F = "..8....13"
    row_G = "....2...."
    row_H = "..98...36"
    row_I = "...3.6.9."
    clues = row_A + row_B + row_C + row_D + row_E + row_F + row_G + row_H + row_I
    game = SquareSudokuGame(Factory9x9(clues))

    game.solve_sudoku()
    game.solve_sudoku()
