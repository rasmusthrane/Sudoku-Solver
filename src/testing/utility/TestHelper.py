from main.app import create_app
from main.framework.game import FormalGameInterface

from typing import List, Tuple
from flask import Flask
from flask.testing import FlaskClient

from main.standard.square_sudoku_game import SquareSudokuGame
from main.variants.factory.factory_4x4 import Factory4x4

class TestHelper:

    @staticmethod
    def printSudoku(game: FormalGameInterface):
        print("=== Sudoku Print ===")
        sudoku = game.grid_values

        for i in range(9):
            row = sudoku[i*9:(i+1)*9]
            for j in range(9):
                print(row[j], end=' ')
                if (j + 1) % 3 == 0 and j < 8:
                    print('|', end=' ')
            print()
            if (i + 1) % 3 == 0 and i < 8:
                print('-'*21)

    @staticmethod
    def printHighlight(any: object):
        RED = "\033[91m"
        BOLD = "\033[1m"
        RESET = "\033[0m"

        print(f"{BOLD}{RED}{'='*20}")
        print(any)
        print(f"{'='*20}{RESET}")

    @staticmethod
    def createAndInjectCluedGameIntoAppForTesting(clues: str) -> Tuple[SquareSudokuGame, Flask, FlaskClient]:
        game = SquareSudokuGame(Factory4x4(clues=clues))
        app: Flask = create_app(game)
        app.testing = True
        client: FlaskClient = app.test_client() # create a test client
        return game, app, client
    
    @staticmethod
    def formatGridValuesAsOneString(grid_values: List[str]) -> str:
        final_str = ""
        for grid_value in grid_values:
            final_str += grid_value
        return final_str
        




if __name__ == "__main__":
    testHelper = TestHelper()
    testHelper.printHighlight("hi")

