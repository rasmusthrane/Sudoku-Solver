from main.standard.SmallSudokuGame import SmallSudokuGame
from main.standard.GameConstants import GameConstants
from testing.utility.TestHelper import TestHelper

import unittest

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = SmallSudokuGame()
        self.testHelper = TestHelper()

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
        correct_cell_names = ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]
        cell_names = list(grid_values_dict.keys())
        self.assertListEqual(cell_names, correct_cell_names)


    

if __name__ == "__main__":
    unittest.main()