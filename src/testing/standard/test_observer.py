from main.standard.SquareSudokuGame import SquareSudokuGame
from main.variants.factory.Factory4by4 import Factory4by4

from testing.standard.doubles.game_observer_spy import GameObserverSpy

import unittest

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = SquareSudokuGame(Factory4by4())
        self.gameObserverSpy = GameObserverSpy()
        self.game.addObserver(self.gameObserverSpy)

    def test_shouldTriggerOnSettingCellValueWhenSettingValue(self):
        self.game.setCellValue('D2', '4')
        self.assertEqual(self.gameObserverSpy.getOnSettingCellValue(), 'placed 4 in D2')

if __name__ == "__main__":
    unittest.main()