from main.standard.GameConstants import GameConstants

from typing import List

def cross(A: str, B: str) -> List[str]:
    "Cross product of strings in A and strings in B."
    return [a + b for a in A for b in B]

def find_duplicates(string: str):
    duplicates = list(set([symbol for symbol in string if symbol != GameConstants.EMPTY_CELL and string.count(symbol) > 1]))
    return duplicates

