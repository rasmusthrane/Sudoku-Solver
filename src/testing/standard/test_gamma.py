from main.framework.gamestate import GameState
from main.framework.status import Status
from main.standard.square_sudoku_game import SquareSudokuGame
from main.standard.game_constants import GameConstants #type:ignore
from main.variants.factory.factory_9x9 import Factory9x9

from testing.utility.TestHelper import TestHelper as th #type:ignore 

from typing import Dict, List
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

    def test_shouldHaveEmptyGridAtStart(self):
        grid_values_dict = self.game.getGridValueDict()
        for v in grid_values_dict.values():
            self.assertEqual(v, GameConstants.EMPTY_CELL)        
    
    def test_shouldReturnStatusOKIfPlacingDigit9InACell(self):
        status = self.game.setCellValue('A1', '9')
        self.assertEqual(status, Status.OK)

    def test_shouldReturnStatusINVALID_CHARIfPlacingDigit11InACell(self):
        status = self.game.setCellValue('I9', '11')
        self.assertEqual(status, Status.INVALID_DIGIT)

    def test_shouldReturnStatusMULTIPLE_CHARACTERSIfPlacingStringContainingMultipleCharactersInACell(self):
        status = self.game.setCellValue('I9', '!!')
        self.assertEqual(status, Status.NOT_A_NUMBER)    

    def test_shouldReturnGameStateOngoingWhenTwoValidRowsArePlaced(self):
        row_A = "123...789"
        row_B = "........."
        row_C = "........."
        row_D = "........."
        row_E = "........."
        row_F = "........."
        row_G = "........."
        row_H = "234.5..9."
        row_I = "........."
        clues = row_A + row_B + row_C + row_D + row_E + row_F + row_G + row_H + row_I
        self.game = SquareSudokuGame(Factory9x9(clues))
        game_state: GameState = self.game.getGameState()
        self.assertEqual(game_state, 'ongoing')

    def test_shouldReturnGameStateOngoingWhenTwoInvalidRowsArePlaced(self):
        row_A = "123...789"
        row_B = "........."
        row_C = "........."
        row_D = "........."
        row_E = "........."
        row_F = "........."
        row_G = "........."
        row_H = "247.5.9.."
        row_I = "........."
        clues = row_A + row_B + row_C + row_D + row_E + row_F + row_G + row_H + row_I
        self.game = SquareSudokuGame(Factory9x9(clues))
        # Place an invalid value
        self.game.setCellValue('H8', '8') 
        game_state: GameState = self.game.getGameState()
        self.assertEqual(game_state, 'constraint_violation')        

    def test_shouldReturnGameStateWonWhenBoardIsFullAndNoConstraintsAreViolated(self):
        row_A = "435269781"
        row_B = "682571493"
        row_C = "197834562"
        row_D = "826195347"
        row_E = "374682915"
        row_F = "951743628"
        row_G = "519326874"
        row_H = "248957136"
        row_I = "763418259"
        clues = row_A + row_B + row_C + row_D + row_E + row_F + row_G + row_H + row_I
        self.game = SquareSudokuGame(Factory9x9(clues))
        game_state: GameState = self.game.getGameState()
        self.assertEqual(game_state, 'won')        

    def test_shouldReturnCorrectCandidatesOnComplicatedBoard(self):
        row_A = ".....3..."
        row_B = "........."
        row_C = "........."
        row_D = "........."
        row_E = "........."
        row_F = "........."
        row_G = "........."
        row_H = "........."
        row_I = "........."
        clues = row_A + row_B + row_C + row_D + row_E + row_F + row_G + row_H + row_I
        self.game = SquareSudokuGame(Factory9x9(clues))

        status1 = self.game.setCellValue('A1', '1')
        status2 = self.game.setCellValue('B4', '2')
        status3 = self.game.setCellValue('C6', '9')
        self.assertTrue(status1 == status2 == status3 == Status.OK)

        self.assertEqual(self.game.candidate_dict['A2'], '2456789')
        self.assertEqual(self.game.candidate_dict['B5'], '145678')
        self.assertEqual(self.game.candidate_dict['D9'], '123456789')

    def test_shouldRaiseErrorWithInvalidClues(self):
        row_A = ".....!..."
        row_B = "........."
        row_C = "........."
        row_D = "........."
        row_E = "........."
        row_F = "........."
        row_G = "........."
        row_H = "........."
        row_I = "........."
        clues = row_A + row_B + row_C + row_D + row_E + row_F + row_G + row_H + row_I

        with self.assertRaises(ValueError) as cm:
            SquareSudokuGame(Factory9x9(clues))
        self.assertIn('Invalid', str(cm.exception))

    def test_shouldRaiseErrorWithTooManyClues(self):
        row_A = "........."
        row_B = "........."
        row_C = "........."
        row_D = "........."
        row_E = "........."
        row_F = "........."
        row_G = "........."
        row_H = "........."
        row_I = ".........." # one clue too many in last row
        clues = row_A + row_B + row_C + row_D + row_E + row_F + row_G + row_H + row_I

        with self.assertRaises(ValueError) as cm:
            SquareSudokuGame(Factory9x9(clues))
        self.assertIn('many', str(cm.exception))
    
    def test_shouldRaiseErrorWithTooFewClues(self):
        row_A = "........."
        row_B = "........."
        row_C = "........."
        row_D = "........."
        row_E = "........."
        row_F = "........."
        row_G = "........."
        row_H = "........."
        row_I = "........" # one clue too few in last row
        clues = row_A + row_B + row_C + row_D + row_E + row_F + row_G + row_H + row_I

        with self.assertRaises(ValueError) as cm:
            SquareSudokuGame(Factory9x9(clues))
        self.assertIn('few', str(cm.exception))

    def test_shouldRaiseErrorWithWhenInjectingCluesThatViolateConstraints(self):
        row_A = "1........"
        row_B = "........."
        row_C = "........."
        row_D = "........."
        row_E = "........."
        row_F = "........."
        row_G = "........."
        row_H = "........."
        row_I = "1........" 
        clues = row_A + row_B + row_C + row_D + row_E + row_F + row_G + row_H + row_I

        with self.assertRaises(ValueError) as cm:
            SquareSudokuGame(Factory9x9(clues))
        self.assertIn('violate', str(cm.exception))
        self.assertIn("Violating cells are ['A1', 'I1']", str(cm.exception))

    def test_shouldSolveEasySudoku(self):
        row_A = "...26.7.1"
        row_B = "68..7..9."
        row_C = "19...45.."
        row_D = "82.1...4."
        row_E = "..46.29.."
        row_F = ".5...3.28"
        row_G = "..93...74"
        row_H = ".4..5..36"
        row_I = "7.3.18..."
        clues = row_A + row_B + row_C + row_D + row_E + row_F + row_G + row_H + row_I
        self.game = SquareSudokuGame(Factory9x9(clues))
        self.game.solveSudoku()
        solution = th.formatGridValuesAsOneString(self.game.getGridValues())

        row_A = "435269781"
        row_B = "682571493"
        row_C = "197834562"
        row_D = "826195347"
        row_E = "374682915"
        row_F = "951743628"
        row_G = "519326874"
        row_H = "248957136"
        row_I = "763418259"
        actual_solution = row_A + row_B + row_C + row_D + row_E + row_F + row_G + row_H + row_I

        self.assertEqual(solution, actual_solution)



if __name__ == "__main__":
    unittest.main()