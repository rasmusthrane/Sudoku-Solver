from main.standard.GameConstants import GameConstants

from typing import List

def cross(A: str, B: str) -> List[str]:
    "Cross product of strings in A and strings in B."
    return [a + b for a in A for b in B]

def find_duplicates(string: str) -> List[str]:
    "Find duplicate characters in a string representation of the sudoku without counting empty cells."
    duplicates = list(set([symbol for symbol in string if symbol != GameConstants.EMPTY_CELL and string.count(symbol) > 1]))
    return duplicates

def find_invalid_characters(string: str) -> List[str]:
    invalid_chars = [char for char in string if char not in GameConstants.VALID_CHARS]
    return invalid_chars
