from main.standard.SquareSudokuGame import SquareSudokuGame
from main.standard.GameConstants import GameConstants
from main.framework.status import Status
from main.variants.factory.Factory4by4 import Factory4by4

from flask import Flask, render_template, request, jsonify


def create_app():
    app = Flask(__name__)

    clues = '...3............'
    game = SquareSudokuGame(Factory4by4(clues=clues))
    grid_value_dict = game.getGridValueDict()
    @app.route('/hello')
    def hello(): # type: ignore
        return f'Hello, World! And the game state is: {grid_value_dict}'
    
    @app.route('/')
    def index(): # type: ignore
        return render_template("template.html", 
                               grid_value_dict=grid_value_dict, 
                               row_letters=game.rows, 
                               col_numbers=game.cols,
                               EMPTY_CELL=GameConstants.EMPTY_CELL,
                               possible_digits=game.possible_digits)
    @app.route('/update_cell', methods=['POST'])
    def update_cell(): #type: ignore
        data = request.get_json()
        cell = data.get('cell')
        value = data.get('value')
        # Attempt to update the game
        status = game.setCellValue(cell, value)
        if status == Status.OK:
            return jsonify(success=True)
        else:
            return jsonify(success=False, error=str(status))


    return app