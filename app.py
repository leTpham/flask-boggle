from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}.
        # Tests below passes before jsoniyfing the return
        # >>> g1 = new_game()
        # >>> len(g1["board"])
        # 5
        # >>> len(games)
        # 1
    """

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return jsonify({"gameId": game_id, "board": game.board})

@app.post("/api/score-word")
def score_word(): # post parameters do not get passed into the view function
    # the only parameters you pass are get query strings
    """Checks if word is legal and scores word if legal
    """

    game_info = request.json
    game_id, word = game_info.values()
    breakpoint()
    game = games[game_id]
    if not game.is_word_in_word_list(word):
        result = "not-word"
    elif not game.check_word_on_board(word):
        result = "not-on-board"
    else:
        result = "ok"

    return jsonify({"result": result})

