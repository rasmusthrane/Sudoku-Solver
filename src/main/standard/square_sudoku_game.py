from main.framework.game import FormalGameInterface
from main.framework.status import Status
from main.framework.utility import cross, find_invalid_characters
from main.variants.factory.game_factory import GameFactory
from main.standard.game_constants import GameConstants
from main.framework.gamestate import GameState

from typing import Tuple, List, Dict, override
import sys #type:ignore

class SquareSudokuGame(FormalGameInterface):
    def __init__(self, gameFactory: GameFactory) -> None:
        sudokuBoardStrategy = gameFactory.createSudokuBoardStrategy()
        self.cols: str = sudokuBoardStrategy.getCols()
        self.rows: str = sudokuBoardStrategy.getRows()
        self.cells: List[str] = cross(self.rows, self.cols)
        self.unitlist: List[List[str]] = sudokuBoardStrategy.getUnitList() 
        self.possible_digits: List[str] = sudokuBoardStrategy.getPossibleDigits()
        self.nrows: int = len(self.rows)
        self.ncols: int = len(self.cols)
        self.nsubgrids: int = sudokuBoardStrategy.getNumberOfSubGrids()
        self.ncells: int = len(self.cells)

        # Create a dict that holds all units that each cell belongs to
        self.units: Dict[str, List[List[str]]] = self._createUnitDict()
        # Create a dict that holds all cells which shares unit with a cell
        self.peers: Dict[str, List[str]] = self._createPeersDict()

        # Initialize grid representation
        self.initial_grid: str = sudokuBoardStrategy.getGridRepresentation()

        # Check if initial injected grid has a valid length
        self._validateInitialGridLength()
        
        # Initialize grid value dict
        self.value_dict: Dict[str, str] = {}
        self._populateInitialValueDict()
        
        # Check if initial injected grid uses valid characters
        self._validateCharactersInInitialGrid()

        # Check if initial injected grid violates any constraints
        self._validateIfAnyConstraintsAreViolated()
            
        # Initialize grid_candidate_dict
        self.candidate_dict: Dict[str, str] = {}
        self._updateCandidateDict()

        # Create list of initial clues
        self.initial_clues: List[str] = self._getCellsWithClues()

        # Set the game state to 'ongoing' and check if any updates have happened
        self.game_state: GameState = 'ongoing'
        self._updateGameState()

    def _validateIfAnyConstraintsAreViolated(self):
        if self._isConstraintViolated():
            violating_cells = self.getViolatingCells()
            raise ValueError(f"Initial clues violate a constraint. Violating cells are {violating_cells}")

    def _validateCharactersInInitialGrid(self):
        invalid_chars = find_invalid_characters(self.initial_grid)
        if invalid_chars:
            raise ValueError(f"Invalid characters in cells: {invalid_chars}")

    def _validateInitialGridLength(self) -> None:
        expected_n_cells = len(self.cells)
        actual_n_cells = len(self.initial_grid)
        if actual_n_cells > expected_n_cells:
            raise ValueError(f"Too many cells. Expected {expected_n_cells} cells, got {actual_n_cells}")
        if actual_n_cells < expected_n_cells:
            raise ValueError(f"Too few cells. Expected {expected_n_cells} cells, got {actual_n_cells}")

    def _createPeersDict(self) -> Dict[str, List[str]]:
        peers: Dict[str, List[str]] = {}
        for c in self.cells:
            all_cells: List[str] = [] # Flattened list to hold all cells that share unit with s
            for unit in self.units[c]:
                all_cells.extend(unit)
            peers_of_c: List[str] = sorted(list(set(all_cells) - set([c])))
            peers[c] = peers_of_c
        return peers

    def _createUnitDict(self) -> Dict[str, List[List[str]]]:
        units: Dict[str, List[List[str]]] = {}
        for c in self.cells:
            units_for_s: List[List[str]] = []  # List to hold units containing s
            for u in self.unitlist:
                if c in u:
                    units_for_s.append(u)
            units[c] = units_for_s
        return units

    def _populateInitialValueDict(self) -> None:
        for i, c in enumerate(self.cells):
            value = self.initial_grid[i]
            self.value_dict[c] = value
    
    def _updateCandidateDict(self) -> None:
        for cell, value in self.value_dict.items():

            # First check if a digit is placed
            digit_placed: bool = value != '.'
            if digit_placed:
                list_of_candidates = list(value) # the only candidate is the value itself

            # Then elimate all possible candidates
            else:
                list_of_candidates = self.possible_digits.copy()
                for peer_of_cell in self.peers[cell]:
                    peer_value_is_candidate: bool = self.value_dict[peer_of_cell] in list_of_candidates
                    if peer_value_is_candidate:
                        list_of_candidates.remove(self.value_dict[peer_of_cell])

            # create string to represent candidates
            self.candidate_dict[cell] = "".join(str(candidate) for candidate in list_of_candidates)           

    def _getCellsWithClues(self) -> List[str]:
        initial_clues: List[str] = []
        for cell, value in self.value_dict.items():
            if value != '.':
                initial_clues.append(cell)
        return initial_clues
    
    def _checkIfCellViolatesConstraint(self, cell:str) -> bool:
        cell_value = self.value_dict[cell]
        if cell_value == GameConstants.EMPTY_CELL:
            return False

        return any(cell_value == self.value_dict[peer] for peer in self.peers[cell])

    def _isConstraintViolated(self) -> bool:
        return any(self._checkIfCellViolatesConstraint(cell) for cell in self.cells)

    def _updateGameState(self) -> None:
        if self._isConstraintViolated():
            self.game_state: GameState = 'constraint_violation'
            return
        
        unique_solution_found: bool = self.getGridValues() == self.getGridCandidateValues()
        if unique_solution_found:
            self.game_state: GameState = 'won'
            return
        
        self.game_state: GameState = 'ongoing'
    @override
    def getViolatingCells(self) -> List[str]:
        violating_cells: List[str] = []
        for cell, cell_value in self.value_dict.items():
            if cell_value == GameConstants.EMPTY_CELL: continue 
            for peer in self.peers[cell]:
                peer_value = self.value_dict[peer]
                if cell_value == peer_value:
                    violating_cells.append(cell)
                    break
        
        return violating_cells

    @override
    def getGameState(self) -> GameState:
        return self.game_state
    @override
    def getSudokuDimension(self) -> Tuple[int, int, int]:
        return self.nrows, self.ncols, self.nsubgrids
    @override
    def getGridValueDict(self) -> Dict[str, str]:
        return self.value_dict
    @override
    def getGridValues(self) -> List[str]:
        return list(self.value_dict.values())
    @override
    def getGridCandidateDict(self) -> Dict[str, str]:
        return self.candidate_dict
    @override
    def getGridCandidateValues(self) -> List[str]:
        return list(self.candidate_dict.values())
    @override
    def getUnits(self) -> Dict[str, List[List[str]]]:
        return self.units

    @override
    def setCellValue(self, cell:str, value:str) -> Status:
        if cell in self.initial_clues:
            return Status.CANNOT_OVERWRITE_CLUE
        if cell not in self.cells:
            return Status.CELL_DOES_NOT_EXIST
        if value not in GameConstants.VALID_CHARS and not value.isnumeric():
            return Status.NOT_A_NUMBER
        if value not in self.possible_digits and value != GameConstants.EMPTY_CELL:
            return Status.INVALID_DIGIT
        
        self.value_dict[cell] = value
        self._updateCandidateDict()
        self._updateGameState()

        return Status.OK
    
    @override
    def removeCellValue(self, cell: str) -> Status:
        status = self.setCellValue(cell, GameConstants.EMPTY_CELL)
        return status
    
    @override
    def solveSudoku(self) -> None:
        self.placeAllSingleCandidateDigits()
        
    def placeAllSingleCandidateDigits(self) -> None:
        while True:
            single_candidate_cells: List[str] = []
            for cell, candidates in self.candidate_dict.items():
                cell_value = self.value_dict[cell]
                if cell_value == GameConstants.EMPTY_CELL and len(candidates) == 1:
                    single_candidate_cells.append(cell)
                    self.setCellValue(cell, candidates)
                
            if len(single_candidate_cells) == 0:
                break

    
if __name__ == "__main__":
    from main.variants.factory.factory_3x3 import Factory3x3 #type:ignore
    from main.variants.factory.factory_4x4 import Factory4x4 #type:ignore
    from main.variants.factory.factory_9x9 import Factory9x9 #type:ignore

    game = SquareSudokuGame(Factory9x9())
    status = game.setCellValue('A1', '11!')
    print(status)
