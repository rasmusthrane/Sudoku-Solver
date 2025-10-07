from main.standard.SquareSudokuGame import SquareSudokuGame
from main.standard.GameConstants import GameConstants
from main.variants.factory.Factory3by3 import Factory3by3
from main.framework.status import Status
from main.framework.GameState import GameState

from testing.utility.TestHelper import TestHelper as th #type:ignore 

import unittest

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = SquareSudokuGame(Factory3by3())

    def test_shouldReturnDimensions3x3x1(self):
        nrows, ncols, nsubgrids = self.game.getSudokuDimension()

        self.assertEqual(nrows, 3)
        self.assertEqual(ncols, 3)
        self.assertEqual(nsubgrids, 1)

    def test_shouldHaveEmptyGridAtStart(self):
        grid_values_dict = self.game.getGridValueDict()
        for v in grid_values_dict.values():
            self.assertEqual(v, GameConstants.EMPTY_CELL)

    def test_shouldHaveCorrectCellNamingInEmptyGrid(self):
        grid_values_dict = self.game.getGridValueDict()
        expected_cell_names = ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]
        cell_names = list(grid_values_dict.keys())

        self.assertListEqual(cell_names, expected_cell_names)

    def test_shouldNotRaiseErrorWhenPassingValidCluesAndCellValuesShouldBeUpdated(self):
        clues = "1.......9"
        try:
            self.game = SquareSudokuGame(Factory3by3(clues))
        except Exception as e:
            self.fail(f"Sudoky3by3() raised {type(e).__name__} unexpectedly!")

        grid_value_dict = self.game.getGridValueDict()
        for cell_name, value in grid_value_dict.items():
            if cell_name == 'A1':
                self.assertEqual(value, '1')
            elif cell_name == 'C3':
                self.assertEqual(value, '9')
            else:
                self.assertEqual(value, GameConstants.EMPTY_CELL)    

    def test_shouldRaiseErrorWithDuplicateClues(self):
        clues = "...3....3" # duplicate 3
        with self.assertRaises(ValueError) as cm:
            SquareSudokuGame(Factory3by3(clues))
        self.assertIn('Duplicate', str(cm.exception))

    def test_shouldRaiseErrorWithInvalidClues(self):
        clues = "..,......" # invalid ,
        with self.assertRaises(ValueError) as cm:
            SquareSudokuGame(Factory3by3(clues))
        self.assertIn('Invalid', str(cm.exception))

    def test_shouldRaiseErrorWithTooManyClues(self):
        clues = ".........." # 10 characters
        with self.assertRaises(ValueError) as cm:
            SquareSudokuGame(Factory3by3(clues))
        self.assertIn('Too many', str(cm.exception))

    def test_shouldRaiseErrorWithTooFewClues(self):
        clues = "........" # 8 characters
        with self.assertRaises(ValueError) as cm:
            SquareSudokuGame(Factory3by3(clues))
        self.assertIn('Too few', str(cm.exception))

    def test_shouldRaiseStatusIfTryingToOverwriteClue(self):
        clues = "1........"
        self.game = SquareSudokuGame(Factory3by3(clues))
        status = self.game.setCellValue('A1', '2')
        self.assertEqual(status, Status.CANNOT_OVERWRITE_CLUE)
    
    def test_shouldRaiseStatusIfUpdatingCellValue(self):
        clues = "1........"
        self.game = SquareSudokuGame(Factory3by3(clues))
        status = self.game.setCellValue('A2', '2')
        self.assertEqual(status, Status.OK)
    
    def test_shouldUpdateCellValueIfValid(self):
        clues = "1........"
        self.game = SquareSudokuGame(Factory3by3(clues))
        self.game.setCellValue('A2', '2')

        grid_value_dict = self.game.getGridValueDict()
        for cell_name, value in grid_value_dict.items():
            if cell_name == 'A1':
                self.assertEqual(value, '1')
            elif cell_name == 'A2':
                self.assertEqual(value, '2')
            else:
                self.assertEqual(value, GameConstants.EMPTY_CELL)    
    
    def test_shouldRaiseStatusIfUpdatingCellWithInvalidChar(self):
        clues = "1........"
        self.game = SquareSudokuGame(Factory3by3(clues))
        status = self.game.setCellValue('A2', '@')
        self.assertEqual(status, Status.INVALID_CHAR)

    def test_shouldReturnOngoingGameWhenStartingEmptyGame(self):
        game_state: GameState = self.game.getGameState()
        self.assertEqual(game_state, 'ongoing')

    def test_shouldReturnWonGameWhenAllCorrectDigitsArePlaced(self):
        clues = "123456789"
        self.game = SquareSudokuGame(Factory3by3(clues))
        game_state: GameState = self.game.getGameState()
        self.assertEqual(game_state, 'won')

    def test_shouldReturnConstraintViolationWhenDuplicateDigitsPlacedInSameUnit(self):
        self.game.setCellValue('A1', '1')
        self.game.setCellValue('A2', '1')
        game_state: GameState = self.game.getGameState()
        self.assertEqual(game_state, 'constraint_violation')
    
    # Given a game, if the player violates a constraint and then fix the violation by removing the digit, the game state 'ongoing' should be returned
    def test_shouldReturnOngoingAfterFixingConstraintViolation(self):
        # First violate a constraint
        self.game.setCellValue('A1', '1')
        self.game.setCellValue('A2', '1')
        game_state: GameState = self.game.getGameState()
        self.assertEqual(game_state, 'constraint_violation')

        # Then fix it
        status = self.game.removeCellValue('A2')

        # Check if game is now 'ongoing' again
        game_state: GameState = self.game.getGameState()
        self.assertEqual(status, Status.OK)
        self.assertEqual(game_state, 'ongoing')

    def test_shouldRaiseErrorWhenUpdatingACellThatDoesNotExist(self):
        status = self.game.setCellValue('A4', '1') #does not exist
        self.assertEqual(status, Status.CELL_DOES_NOT_EXIST)

    def test_shouldRaiseErrorWhenRemovingValueOfCellThatDoesNotExist(self):
        status = self.game.removeCellValue('A4') #does not exist
        self.assertEqual(status, Status.CELL_DOES_NOT_EXIST)

#[] Given a game, when removing the value of cell that does not exist, the status CELL_DOES_NOT_EXIST should be returned        
    
    # def test_allCellsShouldHaveCandidates2Through9ExceptA1WhichHoldsTheClue1(self):
    #     clues = "1........"
    #     self.game.setSudoku(clues)
        
    #     grid_candidate_dict = self.game.getGridCandidateDict()
    #     for cell, candidates in grid_candidate_dict.items():
    #         if cell == "A1":
    #             self.assertEqual(candidates, '')
    #         else:
    #             self.assertEqual(candidates, '23456789')





    

if __name__ == "__main__":
    unittest.main()