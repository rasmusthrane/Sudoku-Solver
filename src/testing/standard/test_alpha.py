from main.standard.square_sudoku_game import SquareSudokuGame
from main.standard.game_constants import GameConstants
from main.variants.factory.factory_3x3 import Factory3x3
from main.framework.status import Status
from main.framework.gamestate import GameState

from testing.utility.TestHelper import TestHelper as th #type:ignore 

import unittest

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = SquareSudokuGame(Factory3x3())

    def test_shouldReturnDimensions3x3x1(self):
        nrows, ncols, nsubgrids = self.game.sudoku_dims

        self.assertEqual(nrows, 3)
        self.assertEqual(ncols, 3)
        self.assertEqual(nsubgrids, 1)

    def test_shouldHaveEmptyGridAtStart(self):
        values_dict = self.game.value_dict
        for v in values_dict.values():
            self.assertEqual(v, GameConstants.EMPTY_CELL)

    def test_shouldHaveCorrectCellNamingInEmptyGrid(self):
        values_dict = self.game.value_dict
        expected_cell_names = ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]
        cell_names = list(values_dict.keys())

        self.assertListEqual(cell_names, expected_cell_names)
    
    def test_shouldOnlyHaveOneUnitInListOfUnits(self):
        self.assertEqual(len(self.game.unitlist),1) 

    def test_shouldNotRaiseErrorWhenPassingValidCluesAndCellValuesShouldBeUpdated(self):
        clues = "1.......9"
        try:
            self.game = SquareSudokuGame(Factory3x3(clues))
        except Exception as e:
            self.fail(f"Sudoky3by3() raised {type(e).__name__} unexpectedly!")

        gridvalue_dict = self.game.value_dict
        for cell_name, value in gridvalue_dict.items():
            if cell_name == 'A1':
                self.assertEqual(value, '1')
            elif cell_name == 'C3':
                self.assertEqual(value, '9')
            else:
                self.assertEqual(value, GameConstants.EMPTY_CELL)    

    def test_shouldRaiseErrorWithDuplicateClues(self):
        clues = "...3....3" # duplicate 3
        with self.assertRaises(ValueError) as cm:
            SquareSudokuGame(Factory3x3(clues))
        self.assertIn('violate', str(cm.exception))
        self.assertIn("Violating cells are ['B1', 'C3']", str(cm.exception))

    def test_shouldRaiseErrorWithInvalidClues(self):
        clues = "..,......" # invalid ,
        with self.assertRaises(ValueError) as cm:
            SquareSudokuGame(Factory3x3(clues))
        self.assertIn('Invalid', str(cm.exception))

    def test_shouldRaiseErrorWithTooManyClues(self):
        clues = ".........." # 10 characters
        with self.assertRaises(ValueError) as cm:
            SquareSudokuGame(Factory3x3(clues))
        self.assertIn('Too many', str(cm.exception))

    def test_shouldRaiseErrorWithTooFewClues(self):
        clues = "........" # 8 characters
        with self.assertRaises(ValueError) as cm:
            SquareSudokuGame(Factory3x3(clues))
        self.assertIn('Too few', str(cm.exception))

    def test_shouldRaiseStatusIfTryingToOverwriteClue(self):
        clues = "1........"
        self.game = SquareSudokuGame(Factory3x3(clues))
        status = self.game.setCellValue('A1', '2')
        self.assertEqual(status, Status.CANNOT_OVERWRITE_CLUE)
    
    def test_shouldRaiseStatusIfUpdatingCellValue(self):
        clues = "1........"
        self.game = SquareSudokuGame(Factory3x3(clues))
        status = self.game.setCellValue('A2', '2')
        self.assertEqual(status, Status.OK)
    
    def test_shouldUpdateCellValueIfValid(self):
        clues = "1........"
        self.game = SquareSudokuGame(Factory3x3(clues))
        self.game.setCellValue('A2', '2')

        gridvalue_dict = self.game.value_dict
        for cell_name, value in gridvalue_dict.items():
            if cell_name == 'A1':
                self.assertEqual(value, '1')
            elif cell_name == 'A2':
                self.assertEqual(value, '2')
            else:
                self.assertEqual(value, GameConstants.EMPTY_CELL)    
    
    def test_shouldRaiseStatusIfUpdatingCellWithInvalidChar(self):
        clues = "1........"
        self.game = SquareSudokuGame(Factory3x3(clues))
        status = self.game.setCellValue('A2', '@')
        self.assertEqual(status, Status.NOT_A_NUMBER)

    def test_shouldReturnOngoingGameWhenStartingEmptyGame(self):
        game_state: GameState = self.game.game_state
        self.assertEqual(game_state, 'ongoing')

    def test_shouldReturnWonGameWhenAllCorrectDigitsArePlaced(self):
        clues = "123456789"
        self.game = SquareSudokuGame(Factory3x3(clues))
        game_state: GameState = self.game.game_state
        self.assertEqual(game_state, 'won')

    def test_shouldReturnConstraintViolationWhenDuplicateDigitsPlacedInSameUnit(self):
        self.game.setCellValue('A1', '1')
        self.game.setCellValue('A2', '1')
        game_state: GameState = self.game.game_state
        self.assertEqual(game_state, 'constraint_violation')
    
    # Given a game, if the player violates a constraint and then fix the violation by removing the digit, the game state 'ongoing' should be returned
    def test_shouldReturnOngoingAfterFixingConstraintViolation(self):
        # First violate a constraint
        self.game.setCellValue('A1', '1')
        self.game.setCellValue('A2', '1')
        game_state: GameState = self.game.game_state
        self.assertEqual(game_state, 'constraint_violation')

        # Then fix it
        status = self.game.removeCellValue('A2')

        # Check if game is now 'ongoing' again
        game_state: GameState = self.game.game_state
        self.assertEqual(status, Status.OK)
        self.assertEqual(game_state, 'ongoing')

    def test_shouldRaiseErrorWhenUpdatingACellThatDoesNotExist(self):
        status = self.game.setCellValue('A4', '1') #does not exist
        self.assertEqual(status, Status.CELL_DOES_NOT_EXIST)

    def test_shouldRaiseErrorWhenRemovingValueOfCellThatDoesNotExist(self):
        status = self.game.removeCellValue('A4') #does not exist
        self.assertEqual(status, Status.CELL_DOES_NOT_EXIST)
    
    def test_shouldPropagateChangesInCandidatesWhenRemovingValueOfCell(self):
        # First set two cell values
        self.game.setCellValue('A1', '1')
        self.game.setCellValue('C3', '2')

        # Then check all cells has correct candidates
        candidate_dict = self.game.candidate_dict
        for cell_name, candidates in candidate_dict.items():
            if cell_name == 'A1':
                self.assertEqual(candidates, '1')
            elif cell_name == 'C3':
                self.assertEqual(candidates, '2')
            else:
                self.assertEqual(candidates, '3456789')

        # Then remove one of the cells 
        self.game.removeCellValue('C3')
        # And check again
        candidate_dict = self.game.candidate_dict
        for cell_name, candidates in candidate_dict.items():
            if cell_name == 'A1':
                self.assertEqual(candidates, '1')
            else:
                self.assertEqual(candidates, '23456789')

if __name__ == "__main__":
    unittest.main()