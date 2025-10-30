from main.framework.utility import find_invalid_characters
from main.variants.factory.game_factory import GameFactory
from main.variants.strategy.sudoku_board import SudokuBoardStrategy
from main.variants.strategy.sudoku_9x9 import Sudoku9x9

class Factory9x9(GameFactory):
    def __init__(self, clues: str = (
        '.........'
        '.........'
        '.........'
        '.........'
        '.........'
        '.........'
        '.........'
        '.........'
        '.........')) -> None:

        if len(clues) > 81:
            raise ValueError(f"Too many characters. Expected 81 characters, got {len(clues)}")
        if len(clues) < 81:
            raise ValueError(f"Too few characters. Expected 81 characters, got {len(clues)}")

        invalid_chars = find_invalid_characters(clues)
        if invalid_chars:
            raise ValueError(f"Invalid characters in clues: {invalid_chars}")

        # duplicates = find_duplicates(clues)
        # if duplicates:
        #     raise ValueError(f"Duplicate values found in clues: {duplicates}")

        self.clues = clues

    def createSudokuBoardStrategy(self) -> SudokuBoardStrategy:
        return Sudoku9x9(self.clues)
    
