from main.standard.square_sudoku_game import SquareSudokuGame
from main.standard.game_constants import GameConstants #type:ignore
from main.variants.factory.factory_9x9 import Factory9x9

from testing.utility.TestHelper import TestHelper as th #type:ignore 

import unittest

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = SquareSudokuGame(Factory9x9())

    def test_shouldReturnDimensions9x9x9(self):
        nrows, ncols, nsubgrids = self.game.getSudokuDimension()

        self.assertEqual(nrows, 9)
        self.assertEqual(ncols, 9)
        self.assertEqual(nsubgrids, 9)

    # def test_shouldHave12UnitsInUnitList(self):
    #     self.assertEqual(len(self.game.unitlist),12) 
    

if __name__ == "__main__":
    unittest.main()