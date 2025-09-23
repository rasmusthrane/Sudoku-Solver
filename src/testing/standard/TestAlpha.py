from main.standard.SmallSudokuGame import SmallSudokuGame
from main.standard.GameConstants import GameConstants
from testing.utility.TestHelper import TestHelper

import unittest
from typing import Dict

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
        grid_values_dict = self.game.getGridValues()
        for v in grid_values_dict.values():
            self.assertEqual(v, GameConstants.EMPTY_CELL)


    

if __name__ == "__main__":
    unittest.main()