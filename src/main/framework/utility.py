from main.standard.game_constants import GameConstants

from typing import List
from math import sqrt

def cross(A: str, B: str) -> List[str]:
    "Cross product of strings in A and strings in B."
    return [a + b for a in A for b in B]

def generate_sudoku_units(rows:str, cols:str, n_subgrids: int) -> List[List[str]]:
    """
    Generate all Sudoku units (rows, columns, and subgrids) for a given grid configuration if the size is a perfect square.

    Each unit is a list of cell labels, such as ['A1', 'A2', ..., 'A9'] for a row unit.
    The function combines all row, column, and box (subgrid) units into a single list.

    Args:
        rows (str): A string representing the row labels (e.g., 'ABCDEFGHI').
        cols (str): A string representing the column labels (e.g., '123456789').
        grid_size (int): The total number of rows/columns in the grid (e.g., 9 for a 9x9 Sudoku).

    Returns:
        List[List[str]]: A list of units, where each unit is a list of cell identifiers.
                         The list includes all row units, column units, and box (subgrid) units.

    Example:
        >>> generate_sudoku_units('ABCDEFGHI', '123456789', 9)
        [['A1','A2',...,'A9'], ['B1','B2',...,'B9'], ..., ['A1','B1',...,'I1'], ..., ['A1','A2','A3','B1','B2','B3','C1','C2','C3'], ...]

    """

    row_units = [[r + c for c in cols] for r in rows]
    col_units = [[r + c for r in rows] for c in cols]

    subgrid_size = int(sqrt(n_subgrids))

    row_groups = [rows[i:i+subgrid_size] for i in range(0, n_subgrids, subgrid_size)]
    col_groups = [cols[i:i+subgrid_size] for i in range(0, n_subgrids, subgrid_size)]
    box_units = [[r + c for r in rg for c in cg] for rg in row_groups for cg in col_groups]

    unitlist = row_units + col_units + box_units
    return unitlist

def find_invalid_characters(string: str) -> List[str]:
    invalid_chars = [char for char in string if char not in GameConstants.VALID_CHARS]
    return invalid_chars
