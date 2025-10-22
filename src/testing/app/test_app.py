from main.framework.status import Status
from main.standard.SquareSudokuGame import SquareSudokuGame
from main.standard.GameConstants import GameConstants #type:ignore
from main.variants.factory.Factory4by4 import Factory4by4
from main.app import create_app

from testing.utility.TestHelper import TestHelper as th #type:ignore 

import unittest
import json

class TestFlaskGUI(unittest.TestCase):
    def setUp(self):
        self.game = SquareSudokuGame(Factory4by4())
        self.app = create_app(self.game)
        self.app.testing = True
        self.client = self.app.test_client() # create a test client

    def test_shouldReturnStatusOKWhenClientPlaces1inA1AndShouldPropagateValueChangeToGame(self):
        payload = {'cell': 'A1', 'value': '1'}
        # Let client update cell
        response = self.client.post('/update_cell',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        response_dict = json.loads(response.data)
        
        # Check that the response is as expected
        self.assertEqual(response_dict['cell'], 'A1')
        self.assertEqual(response_dict['value'], '1')
        self.assertEqual(response_dict['game_update_status'], Status.OK.name)

        # And that the change of value propagates
        value_of_A1 = self.game.getGridValueDict()['A1']
        self.assertEqual(value_of_A1, '1')


        

if __name__ == "__main__":
    unittest.main()