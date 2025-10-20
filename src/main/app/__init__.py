from main.standard.SquareSudokuGame import SquareSudokuGame
from main.variants.factory.Factory4by4 import Factory4by4

from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    game = SquareSudokuGame(Factory4by4())

    @app.route('/hello')
    def hello(): # type: ignore
        return f'Hello, World! And the game state is: {game.getGameState()}'
    
    @app.route('/')
    def index(): # type: ignore
        return render_template("template.html")

    return app