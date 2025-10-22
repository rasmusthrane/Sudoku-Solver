from main.app import create_app
from main.framework.game import FormalGameInterface

from typing import Tuple
from flask import Flask
from flask.testing import FlaskClient

from main.standard.SquareSudokuGame import SquareSudokuGame
from main.variants.factory.Factory4by4 import Factory4by4

class TestHelper:

    @staticmethod
    def printGameState(game: FormalGameInterface):
        print("=== Game State Print ===")

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
        game = SquareSudokuGame(Factory4by4(clues=clues))
        app: Flask = create_app(game)
        app.testing = True
        client: FlaskClient = app.test_client() # create a test client
        return game, app, client




if __name__ == "__main__":
    testHelper = TestHelper()
    testHelper.printHighlight("hi")

