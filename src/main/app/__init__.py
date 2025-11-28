from typing import Dict
from main.framework.status import Status
from main.standard.square_sudoku_game import SquareSudokuGame
from main.standard.game_constants import GameConstants
from main.variants.factory.factory_9x9 import Factory9x9

from flask import Flask, jsonify, render_template, request
from math import sqrt


def create_app(game: SquareSudokuGame | None = None) -> Flask:
    app = Flask(__name__)

    # Default behaviour if no clues are injected
    if game is None:
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
        game = SquareSudokuGame(Factory9x9(clues=clues))      
    
    @app.route('/')
    def index(): # type: ignore
        return render_template("template.html", 
                               value_dict=game.value_dict, 
                               row_letters=game.rows, 
                               col_numbers=game.cols,
                               n_subgrids=game.nsubgrids,
                               n=int(sqrt(game.nsubgrids)),
                               EMPTY_CELL=GameConstants.EMPTY_CELL,
                               possible_digits=game.possible_digits,
                               initial_clues=game.initial_clues)
    
    @app.route('/update_cell', methods=['POST'])
    def update_cell(): #type: ignore
        data = request.get_json()
        cell = data.get('cell')
        value = data.get('value')
        
        if value == "":
            status: Status = game.remove_cell_value(cell)
        else:
            status: Status = game.set_cell_value(cell, value)
        
        response: Dict[str, str] = {
            'game_update_status': status.name,
            'cell': cell,
            'value': value
            }
        
        return jsonify(response)
    
    @app.route('/get_game_state', methods=['GET'])
    def get_game_state(): #type: ignore
        return jsonify({
            'game_state': game.game_state,
            'violating_cells': game.compute_violating_cells()
            })

    return app