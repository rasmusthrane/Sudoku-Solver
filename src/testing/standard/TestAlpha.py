from main.standard.SquareSudokuGame import SquareSudokuGame
from main.standard.GameConstants import GameConstants
from main.framework.status import Status
from testing.utility.TestHelper import TestHelper as th

import unittest

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = SquareSudokuGame()

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
    
    def test_shouldHaveCorrectValuesAfterInjectingCluesAndStatusShouldBeOK(self):
        clues = "1.......9"
        status = self.game.setSudoku(clues)

        grid_values_dict = self.game.getGridValueDict()
        cell_values = list(grid_values_dict.values())
        expected_values = ['1', '.', '.', '.', '.', '.', '.', '.', '9']

        self.assertListEqual(cell_values, expected_values)
        self.assertIs(status, Status.OK)

    def test_shouldRejectClueInjectionWhenDuplicateCluesAndStatusShouldBeDUPLICATE_CLUE(self):
        clues = "...3..3.."
        status = self.game.setSudoku(clues)
        
        grid_values_dict = self.game.getGridValueDict()
        cell_values = list(grid_values_dict.values())
        expected_values = ['.', '.', '.', '.', '.', '.', '.', '.', '.']

        self.assertListEqual(cell_values, expected_values)
        self.assertIs(status, Status.DUPLICATE_CLUE)



    

if __name__ == "__main__":
    unittest.main()