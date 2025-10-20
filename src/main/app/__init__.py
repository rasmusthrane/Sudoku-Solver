from main.standard.SquareSudokuGame import SquareSudokuGame
from main.variants.factory.Factory4by4 import Factory4by4
from main.standard.GameConstants import GameConstants

from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    clues = '...3............'
    game = SquareSudokuGame(Factory4by4(clues=clues))
    grid_value_dict = game.getGridValueDict()
    @app.route('/hello')
    def hello(): # type: ignore
        return f'Hello, World! And the game state is: {game.cols}'
    
    @app.route('/')
    def index(): # type: ignore
        return render_template("template.html", 
                               grid_value_dict=grid_value_dict, 
                               row_letters=game.rows, 
                               col_numbers=game.cols,
                               EMPTY_CELL = GameConstants.EMPTY_CELL)

    return app