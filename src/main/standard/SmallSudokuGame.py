from main.framework.game import FormalGameInterface
from main.framework.utility import cross

from typing import Tuple, List, Dict, Set
from typing_extensions import Literal

class SmallSudokuGame(FormalGameInterface):
    def __init__(self) -> None:
        self.cols = "123"
        self.rows = "ABC"
        self.squares = cross(self.rows, self.cols)
        self.unitlist = ([cross(self.rows, self.cols)]) # Only one unit in small sudoku 

        # Create a dict that holds all units that each square belongs to
        self.units: Dict[str, List[List[str]]] = {}
        for s in self.squares:
            units_for_s: List[List[str]] = []  # List to hold units containing s
            for u in self.unitlist:
                if s in u:
                    units_for_s.append(u)
            self.units[s] = units_for_s

        # Create a dict that holds all squares which shares unit with a square
        self.peers: Dict[str, Set[str]] = {}
        for s in self.squares:
            all_squares: List[str] = [] # Flattened list to hold all squares that share unit with s
            for unit in self.units[s]:
                all_squares.extend(unit)
            peers_of_s: Set[str] = set(all_squares) - set([s])
            self.peers[s] = peers_of_s
        
        self.nrows = len(self.rows)
        self.ncols = len(self.cols)
        self.nsubgrids = 1 # Todo: Infer from nrows, ncols

    def getWinStatus(self) -> Literal["win", "ongoing"]:
        return "win"
    
    def getSudokuDimension(self) -> Tuple[int, int, int]:
        return self.nrows, self.ncols, self.nsubgrids

if __name__ == "__main__":
    game = SmallSudokuGame()