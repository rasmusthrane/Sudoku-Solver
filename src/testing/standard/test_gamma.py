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
        nrows, ncols, nsubgrids = self.game.sudoku_dims

        self.assertEqual(nrows, 9)
        self.assertEqual(ncols, 9)
        self.assertEqual(nsubgrids, 9)

    def test_shouldHave27UnitsInUnitList(self):
        self.assertEqual(len(self.game.all_units),27) 

    def test_unitsOfA1AreCorrect(self):
        units: Dict[str, List[List[str]]] = self.game.units
        expected_units = sorted([
            ['A1','A2','A3','A4','A5','A6','A7','A8','A9'], 
            ['A1','B1','C1','D1','E1','F1','G1','H1','I1'], 
            ['A1','A2','A3','B1','B2','B3','C1','C2','C3']
            ]) # sort ensures that the two lists can be compared
        self.assertListEqual(sorted(units['A1']), expected_units)        

    def test_shouldHaveEmptyGridAtStart(self):
        value_dict = self.game.value_dict
        for v in value_dict.values():
            self.assertEqual(v, GameConstants.EMPTY_CELL)        
    
    def test_shouldReturnStatusOKIfPlacingDigit9InACell(self):
        status = self.game.set_cell_value('A1', '9')
        self.assertEqual(status, Status.OK)

    def test_shouldReturnStatusINVALID_CHARIfPlacingDigit11InACell(self):
        status = self.game.set_cell_value('I9', '11')
        self.assertEqual(status, Status.INVALID_DIGIT)

    def test_shouldReturnStatusMULTIPLE_CHARACTERSIfPlacingStringContainingMultipleCharactersInACell(self):
        status = self.game.set_cell_value('I9', '!!')
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
        game_state: GameState = self.game.game_state
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
        self.game.set_cell_value('H8', '8') 
        game_state: GameState = self.game.game_state
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
        game_state: GameState = self.game.game_state
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

        status1 = self.game.set_cell_value('A1', '1')
        status2 = self.game.set_cell_value('B4', '2')
        status3 = self.game.set_cell_value('C6', '9')
        self.assertTrue(status1 == status2 == status3 == Status.OK)

        self.assertEqual(self.game.candidates_of('A2'), '2456789')
        self.assertEqual(self.game.candidates_of('B5'), '145678')
        self.assertEqual(self.game.candidates_of('D9'), '123456789')

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

    def test_shouldSolveEasySudoku1(self):
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
        self.game.solve_sudoku()
        solution = th.formatGridValuesAsOneString(self.game.grid_values)
        
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

    def test_shouldSolveEasySudoku2(self):
        row_A = "1..489..6"
        row_B = "73.....4."
        row_C = ".....1295"
        row_D = "..712.6.."
        row_E = "5..7.3..8"
        row_F = "..6.957.."
        row_G = "9146....."
        row_H = ".2.....37"
        row_I = "8..512..4"
        clues = row_A + row_B + row_C + row_D + row_E + row_F + row_G + row_H + row_I
        self.game = SquareSudokuGame(Factory9x9(clues))
        self.game.solve_sudoku()
        solution = th.formatGridValuesAsOneString(self.game.grid_values)

        row_A = "152489376"
        row_B = "739256841"
        row_C = "468371295"
        row_D = "387124659"
        row_E = "591763428"
        row_F = "246895713"
        row_G = "914637582"
        row_H = "625948137"
        row_I = "873512964"
        actual_solution = row_A + row_B + row_C + row_D + row_E + row_F + row_G + row_H + row_I

        self.assertEqual(solution, actual_solution)

    def test_shouldDetectNakedPairAndEliminateCandidates(self):
        row_A = "63......4"
        row_B = ".4......."
        row_C = "..29....5"
        row_D = ".9......."
        row_E = "...2..36."
        row_F = "8...6..5."
        row_G = ".64.8..27"
        row_H = "58.3....."
        row_I = ".....1..." 
        clues = row_A + row_B + row_C + row_D + row_E + row_F + row_G + row_H + row_I
        self.game = SquareSudokuGame(Factory9x9(clues))

        # First check if candidates are correct before eliminating some candidates
        self.assertEqual(self.game.candidates_of('A3'), '15789')
        self.assertEqual(self.game.candidates_of('B1'), '179')
        self.assertEqual(self.game.candidates_of('B3'), '15789')
        self.assertEqual(self.game.candidates_of('C1'), '17') # naked pair
        self.assertEqual(self.game.candidates_of('C2'), '17') # naked pair

        # Then apply naked pair elimination and check candidates
        self.game._apply_naked_pair_elimination_on(unit=['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']) # pyright: ignore[reportPrivateUsage]
        self.assertEqual(self.game.candidates_of('A3'), '589')
        self.assertEqual(self.game.candidates_of('B1'), '9')
        self.assertEqual(self.game.candidates_of('B3'), '589')
        self.assertEqual(self.game.candidates_of('C1'), '17') 
        self.assertEqual(self.game.candidates_of('C2'), '17') 

        # At this point the cell should still be empty as we are only eliminating candidates
        self.assertEqual(self.game.value_of('B1'), GameConstants.EMPTY_CELL)


    def test_shouldNotElimateCandidatesIfNotANakedPair(self):
        row_A = "63......4"
        row_B = ".4......."
        row_C = "..29....5"
        row_D = ".9......."
        row_E = "...2..36."
        row_F = "8...6..5."
        row_G = ".64.8..27"
        row_H = "58.3....."
        row_I = ".....1..." 
        clues = row_A + row_B + row_C + row_D + row_E + row_F + row_G + row_H + row_I
        self.game = SquareSudokuGame(Factory9x9(clues))

        # First check if candidates are correct
        self.assertEqual(self.game.candidates_of('G4'), '5')
        self.assertEqual(self.game.candidates_of('G6'), '59') # not a pair, just a candidate with two digits
        self.assertEqual(self.game.candidates_of('H5'), '2479')
        self.assertEqual(self.game.candidates_of('H6'), '24679') 
        self.assertEqual(self.game.candidates_of('I4'), '4567') 
        self.assertEqual(self.game.candidates_of('I5'), '24579') 

        # Then check what we get wen eliminating the unit
        self.game._apply_naked_pair_elimination_on(unit=['G4', 'G5', 'G6', 'H4', 'H5', 'H6', 'I4', 'I5', 'I6']) # pyright: ignore[reportPrivateUsage]
        self.assertEqual(self.game.candidates_of('G4'), '5')
        self.assertEqual(self.game.candidates_of('G6'), '59') # should still have value 59
        self.assertEqual(self.game.candidates_of('H5'), '2479')
        self.assertEqual(self.game.candidates_of('H6'), '24679') 
        self.assertEqual(self.game.candidates_of('I4'), '4567') 
        self.assertEqual(self.game.candidates_of('I5'), '24579') 

    def test_shouldSolveIntermediateSudoku1(self):
        row_A = ".2.6.8..."
        row_B = "58...97.."
        row_C = "....4...."
        row_D = "37....5.."
        row_E = "6.......4"
        row_F = "..8....13"
        row_G = "....2...."
        row_H = "..98...36"
        row_I = "...3.6.9."
        clues = row_A + row_B + row_C + row_D + row_E + row_F + row_G + row_H + row_I
        self.game = SquareSudokuGame(Factory9x9(clues))
        self.game.solve_sudoku()
        solution = th.formatGridValuesAsOneString(self.game.grid_values)

        row_A = "123678945"
        row_B = "584239761"
        row_C = "967145328"
        row_D = "372461589"
        row_E = "691583274"
        row_F = "458792613"
        row_G = "836924157"
        row_H = "219857436"
        row_I = "745316892"
        actual_solution = row_A + row_B + row_C + row_D + row_E + row_F + row_G + row_H + row_I

        self.assertEqual(solution, actual_solution)

    def test_shouldSolveIntermediateSudoku2(self):
        row_A = ".....4..."
        row_B = "...17.6.."
        row_C = "48.3561.."
        row_D = "..4..75.."
        row_E = "....1.7.."
        row_F = "5...2..34"
        row_G = "95......6"
        row_H = "12......8"
        row_I = "........." 
        clues = row_A + row_B + row_C + row_D + row_E + row_F + row_G + row_H + row_I
        self.game = SquareSudokuGame(Factory9x9(clues))
        self.game.solve_sudoku()
        solution = th.formatGridValuesAsOneString(self.game.grid_values)

        row_A = "615294387"
        row_B = "392178645"
        row_C = "487356129"
        row_D = "264837591"
        row_E = "839415762"
        row_F = "571629834"
        row_G = "953782416"
        row_H = "126543978"
        row_I = "748961253" 

        actual_solution = row_A + row_B + row_C + row_D + row_E + row_F + row_G + row_H + row_I

        self.assertEqual(solution, actual_solution)

if __name__ == "__main__":
    unittest.main()