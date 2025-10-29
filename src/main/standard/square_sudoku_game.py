from main.framework.game import FormalGameInterface
from main.framework.status import Status
from main.framework.utility import cross
from main.variants.factory.game_factory import GameFactory
from main.standard.game_constants import GameConstants
from main.framework.gamestate import GameState

from typing import Tuple, List, Dict, override
import sys #type:ignore

class SquareSudokuGame(FormalGameInterface):
    def __init__(self, gameFactory: GameFactory) -> None:
        sudokuBoardStrategy = gameFactory.createSudokuBoardStrategy()
        self.cols = sudokuBoardStrategy.getCols()
        self.rows = sudokuBoardStrategy.getRows()
        self.cells: List[str] = cross(self.rows, self.cols)
        self.unitlist = sudokuBoardStrategy.getUnitList() 
        self.possible_digits = sudokuBoardStrategy.getPossibleDigits()

        # Create a dict that holds all units that each cell belongs to
        self.units = self.__createUnitDict()
        # Create a dict that holds all cells which shares unit with a cell
        self.peers = self.__createPeersDict()
        
        self.nrows = len(self.rows)
        self.ncols = len(self.cols)
        self.nsubgrids = sudokuBoardStrategy.getNumberOfSubGrids()
        self.ncells = len(self.cells)

        # Initialize grid representation
        self.initial_grid = sudokuBoardStrategy.getGridRepresentation()

        # Initialize grid value dict
        self.grid_value_dict: Dict[str, str] = {}
        self.__populateInitialGridValueDict()

        # Initialize grid_candidate_dict
        self.grid_candidate_dict: Dict[str, str] = {}
        self.__updateGridCandidateDict()

        # Create list of initial clues
        self.initial_clues: List[str] = self.__getCellsWithClues()

        self.game_state: GameState = 'ongoing'
        self.__updateGameState()

    def __createPeersDict(self) -> Dict[str, List[str]]:
        peers: Dict[str, List[str]] = {}
        for c in self.cells:
            all_cells: List[str] = [] # Flattened list to hold all cells that share unit with s
            for unit in self.units[c]:
                all_cells.extend(unit)
            peers_of_c: List[str] = sorted(list(set(all_cells) - set([c])))
            peers[c] = peers_of_c
        return peers

    def __createUnitDict(self) -> Dict[str, List[List[str]]]:
        units: Dict[str, List[List[str]]] = {}
        for c in self.cells:
            units_for_s: List[List[str]] = []  # List to hold units containing s
            for u in self.unitlist:
                if c in u:
                    units_for_s.append(u)
            units[c] = units_for_s
        return units

    def __populateInitialGridValueDict(self) -> None:
        for i, c in enumerate(self.cells):
            value = self.initial_grid[i]
            self.grid_value_dict[c] = value
    
    def __updateGridCandidateDict(self) -> None:
        for cell, value in self.grid_value_dict.items():

            # First check if a digit is placed
            digit_placed: bool = value != '.'
            if digit_placed:
                list_of_candidates = list(value) # the only candidate is the value itself

            # Then elimate all possible candidates
            else:
                list_of_candidates = self.possible_digits.copy()
                for peer_of_cell in self.peers[cell]:
                    peer_value_is_candidate: bool = self.grid_value_dict[peer_of_cell] in list_of_candidates
                    if peer_value_is_candidate:
                        list_of_candidates.remove(self.grid_value_dict[peer_of_cell])

            # create string to represent candidates
            self.grid_candidate_dict[cell] = "".join(str(candidate) for candidate in list_of_candidates)           

    def __getCellsWithClues(self) -> List[str]:
        initial_clues: List[str] = []
        for cell, value in self.grid_value_dict.items():
            if value != '.':
                initial_clues.append(cell)
        return initial_clues
    
    def __checkIfCellViolatesConstraint(self, cell:str) -> bool:
        cell_value = self.grid_value_dict[cell]
        if cell_value == GameConstants.EMPTY_CELL:
            return False

        return any(cell_value == self.grid_value_dict[peer] for peer in self.peers[cell])

    def __isConstraintsViolated(self) -> bool:
        return any(self.__checkIfCellViolatesConstraint(cell) for cell in self.cells)

    def __updateGameState(self) -> None:
        if self.__isConstraintsViolated():
            self.game_state: GameState = 'constraint_violation'
            return
        
        unique_solution_found: bool = self.getGridValues() == self.getGridCandidateValues()
        if unique_solution_found:
            self.game_state: GameState = 'won'
            return
        
        self.game_state: GameState = 'ongoing'

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
        return self.grid_candidate_dict
    @override
    def getGridCandidateValues(self) -> List[str]:
        return list(self.grid_candidate_dict.values())
    @override
    def getUnits(self) -> Dict[str, List[List[str]]]:
        return self.units

    @override
    def setCellValue(self, cell:str, value:str) -> Status:
        if cell in self.initial_clues:
            return Status.CANNOT_OVERWRITE_CLUE
        if cell not in self.cells:
            return Status.CELL_DOES_NOT_EXIST
        if value not in GameConstants.VALID_CHARS:
            return Status.INVALID_CHAR
        if value not in self.possible_digits and value != GameConstants.EMPTY_CELL:
            return Status.INVALID_DIGIT
        
        self.grid_value_dict[cell] = value
        self.__updateGridCandidateDict()
        self.__updateGameState()

        return Status.OK
    
    @override
    def removeCellValue(self, cell: str) -> Status:
        status = self.setCellValue(cell, GameConstants.EMPTY_CELL)
        return status
    
if __name__ == "__main__":
    from main.variants.factory.factory_3x3 import Factory3by3 #type:ignore
    from main.variants.factory.factory_4x4 import Factory4by4 #type:ignore

    clues = "12343432........"
    print(f"clues: {clues}")
    game = SquareSudokuGame(Factory4by4(clues))
    game_state: GameState = game.getGameState()
