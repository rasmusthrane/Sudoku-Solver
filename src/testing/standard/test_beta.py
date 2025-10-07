from main.standard.SquareSudokuGame import SquareSudokuGame
from main.standard.GameConstants import GameConstants #type:ignore
from main.variants.factory.Factory4by4 import Factory4by4

from testing.utility.TestHelper import TestHelper as th #type:ignore 

import unittest

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = SquareSudokuGame(Factory4by4())

    def test_shouldReturnDimensions4x4x4(self):
        nrows, ncols, nsubgrids = self.game.getSudokuDimension()

        self.assertEqual(nrows, 4)
        self.assertEqual(ncols, 4)
        self.assertEqual(nsubgrids, 4)
    
    def test_unitsOfA1AreCorrect(self):
        pass

    # def test_shouldHaveEmptyGridAtStart(self):
    #     grid_values_dict = self.game.getGridValueDict()
    #     for v in grid_values_dict.values():
    #         self.assertEqual(v, GameConstants.EMPTY_CELL)

    # def test_shouldHaveCorrectCellNamingInEmptyGrid(self):
    #     grid_values_dict = self.game.getGridValueDict()
    #     expected_cell_names = ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]
    #     cell_names = list(grid_values_dict.keys())

    #     self.assertListEqual(cell_names, expected_cell_names)


if __name__ == "__main__":
    unittest.main()