from typing import Dict, List
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

    def test_shouldHave27UnitsInUnitList(self):
        self.assertEqual(len(self.game.unitlist),27) 

    def test_unitsOfA1AreCorrect(self):
        units: Dict[str, List[List[str]]] = self.game.getUnits()
        expected_units = sorted([
            ['A1','A2','A3','A4','A5','A6','A7','A8','A9'], 
            ['A1','B1','C1','D1','E1','F1','G1','H1','I1'], 
            ['A1','A2','A3','B1','B2','B3','C1','C2','C3']
            ]) # sort ensures that the two lists can be compared
        self.assertListEqual(sorted(units['A1']), expected_units)        

    

if __name__ == "__main__":
    unittest.main()