from main.standard.SquareSudokuGame import SquareSudokuGame
from main.standard.GameConstants import GameConstants
from main.variants.factory.Factory4by4 import Factory4by4

from flask import Flask, render_template, request, jsonify
#import json


def create_app():
    app = Flask(__name__)

    clues = '...3............'
    game = SquareSudokuGame(Factory4by4(clues=clues))
    grid_value_dict = game.getGridValueDict()
    @app.route('/hello')
    def hello(): # type: ignore
        return f'Hello, World! And the game state is: {game.possible_digits}'
    
    @app.route('/')
    def index(): # type: ignore
        return render_template("template.html", 
                               grid_value_dict=grid_value_dict, 
                               row_letters=game.rows, 
                               col_numbers=game.cols,
                               EMPTY_CELL=GameConstants.EMPTY_CELL,
                               possible_digits=game.possible_digits,
                               initial_clues=game.initial_clues)
    @app.route('/update_cell', methods=['POST'])
    def update_cell(): #type: ignore
        data = request.get_json()
        cell = data.get('cell')
        value = data.get('value')
        
        if value == "":
            game.removeCellValue(cell)
        else:
            game.setCellValue(cell, value)
        
        return jsonify({"status": "success", "cell": cell, "value": value})


    return app