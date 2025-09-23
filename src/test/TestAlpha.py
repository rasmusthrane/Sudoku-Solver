from main.standard.SmallSudokuGame import SmallSudokuGame

import unittest

class TestGame(unittest.TestCase):
    def setUp(self) -> None:
        self.game = SmallSudokuGame()

    def test_shouldReturnDimensions3x3x1(self):
        nrows, ncols, nsubgrids = self.game.getSudokuDimension()
        self.assertEqual(nrows, 3)
        self.assertEqual(ncols, 3)
        self.assertEqual(nsubgrids, 1)

if __name__ == "__main__":
    unittest.main()