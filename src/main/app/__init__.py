from main.standard.square_sudoku_game import SquareSudokuGame
from main.standard.game_constants import GameConstants
from main.framework.status import Status
from main.variants.factory.factory_4x4 import Factory4x4

from flask import Flask, render_template, request, jsonify

from typing import Dict


def create_app(game: SquareSudokuGame | None = None) -> Flask:
    app = Flask(__name__)

    # Default behaviour if no clues are injected
    if game is None:
        game = SquareSudokuGame(Factory4x4(clues='1...............'))
    #app.config['game'] = game         

    grid_value_dict = game.getGridValueDict()
    @app.route('/hello')
    def hello(): # type: ignore
        return f'Hello, World! And the game state is: {game.initial_grid}'
    
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
            status: Status = game.removeCellValue(cell)
        else:
            status: Status = game.setCellValue(cell, value)
        
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
            'violating_cells': game.getViolatingCells()
            })


    return app