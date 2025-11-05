from main.standard.square_sudoku_game import SquareSudokuGame
from main.standard.game_constants import GameConstants #type:ignore
from main.variants.factory.factory_4x4 import Factory4x4
from main.framework.status import Status
from main.framework.gamestate import GameState

from testing.utility.TestHelper import TestHelper as th #type:ignore 

import unittest
from typing import List, Dict

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = SquareSudokuGame(Factory4x4())

    def test_shouldReturnDimensions4x4x4(self):
        nrows, ncols, nsubgrids = self.game.sudoku_dims

        self.assertEqual(nrows, 4)
        self.assertEqual(ncols, 4)
        self.assertEqual(nsubgrids, 4)

    def test_shouldHave12UnitsInUnitList(self):
        self.assertEqual(len(self.game.all_units),12) 
    
    def test_unitsOfA1AreCorrect(self):
        units: Dict[str, List[List[str]]] = self.game.units
        expected_units = sorted([['A1','A2','B1','B2'], ['A1','A2','A3','A4'], ['A1','B1','C1','D1']]) # sort ensures that the two lists can be compared
        self.assertListEqual(sorted(units['A1']), expected_units)        

    def test_shouldHaveEmptyGridAtStart(self):
        value_dict = self.game.value_dict
        for v in value_dict.values():
            self.assertEqual(v, GameConstants.EMPTY_CELL)

    def test_shouldHaveCorrectCellNamingInEmptyGrid(self):
        value_dict = self.game.value_dict
        expected_cell_names = ["A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4", "D1", "D2", "D3", "D4"]
        cell_names = list(value_dict.keys())

        self.assertListEqual(cell_names, expected_cell_names)

    def test_shouldHaveCorrectCandidatesAfterPlacingSomeValues(self):
        status1 = self.game.set_cell_value('A1', '1')
        status2 = self.game.set_cell_value('A2', '2')
        status3 = self.game.set_cell_value('B2', '3')
        self.assertTrue(status1 == status2 == status3 == Status.OK)
        
        self.assertEqual(self.game.candidates_of('B1'), '4')
        self.assertEqual(self.game.candidates_of('A3'), '34')
        self.assertEqual(self.game.candidates_of('A4'), '34')
        self.assertEqual(self.game.candidates_of('B3'), '124')
        self.assertEqual(self.game.candidates_of('B4'), '124')
        self.assertEqual(self.game.candidates_of('D3'), '1234')
    
    def test_shouldHaveCorrectCandidatesAfterRemovingCellValue(self):
        # First place some values
        status1 = self.game.set_cell_value('A1', '1')
        status2 = self.game.set_cell_value('A4', '2')
        status3 = self.game.set_cell_value('D4', '3')
        # check everything alright
        self.assertTrue(status1 == status2 == status3 == Status.OK)
        self.assertEqual(self.game.candidates_of('A4'), '2')

        # Then remove the value from a cell
        status4 = self.game.remove_cell_value('A4')
        # and check that everything is still alright
        self.assertEqual(status4, Status.OK)
        self.assertEqual(self.game.candidates_of('A4'), '24')

    def test_shouldReturnStatusINVALID_CHARIfPlacingDigit9InACell(self):
        status = self.game.set_cell_value('A1', '9')
        self.assertEqual(status, Status.INVALID_DIGIT)
    
    def test_shouldReturnGameStateOngoingWhenTwoValidRowsArePlaced(self):
        row_A = "1234"
        row_B = "3412"
        row_C = "...."
        row_D = "...."
        clues = row_A + row_B + row_C + row_D
        self.game = SquareSudokuGame(Factory4x4(clues))
        game_state: GameState = self.game.game_state
        self.assertEqual(game_state, 'ongoing')

        # check that no violating cells are found
        violating_cells = self.game.compute_violating_cells()
        self.assertListEqual(violating_cells, [])

    def test_shouldReturnGameStateConstraintViolationWhenAnInvalidRowIsPlacedAndGiveListOfViolatingCells(self):
        row_A = "1234"
        row_B = ".3.1" 
        row_C = "...."
        row_D = "...."
        clues = row_A + row_B + row_C + row_D
        self.game = SquareSudokuGame(Factory4x4(clues))
        # Place invalid values
        self.game.set_cell_value('B1', '2')
        self.game.set_cell_value('B3', '4')
        game_state: GameState = self.game.game_state
        self.assertEqual(game_state, 'constraint_violation')    

        violating_cells = self.game.compute_violating_cells()
        self.assertListEqual(sorted(violating_cells), ['A2', 'A4', 'B1', 'B3'])   

    def test_shouldReturnGameStateWonWhenFourValidRowsArePlaced(self):
        row_A = "1234"
        row_B = "3412"
        row_C = "4321"
        row_D = "2143"
        clues = row_A + row_B + row_C + row_D
        self.game = SquareSudokuGame(Factory4x4(clues))
        game_state: GameState = self.game.game_state
        self.assertEqual(game_state, 'won')    

        # check that no violating cells are found
        violating_cells = self.game.compute_violating_cells()
        self.assertListEqual(violating_cells, [])
        

    def test_shouldReturnGameStateConstraintViolationWhenThreeValidRowsAndOneInvalidRowArePlacedAndGiveListOfViolatingCells(self):
        row_A = "1234"
        row_B = "3412"
        row_C = "4321"
        row_D = "2..." # invalid
        clues = row_A + row_B + row_C + row_D
        self.game = SquareSudokuGame(Factory4x4(clues))
        # Place an invalid row
        self.game.set_cell_value('D2', '2')
        self.game.set_cell_value('D3', '3')
        self.game.set_cell_value('D4', '4')
        game_state: GameState = self.game.game_state
        self.assertEqual(game_state, 'constraint_violation')     

        violating_cells = self.game.compute_violating_cells()
        self.assertListEqual(sorted(violating_cells), ['A2', 'A3', 'A4', 'D1', 'D2', 'D3', 'D4'])   



if __name__ == "__main__":
    unittest.main()