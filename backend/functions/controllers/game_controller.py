# This file will contain the business logic for game-related endpoints.
from services.game_service import GameService
import json
from datetime import datetime
from firebase_functions import https_fn

def start_game_controller(request: https_fn.Request):
    """Handles the logic for starting a new game."""
    game_service = GameService() # Instantiate GameService inside the function
    try:
        data = request.get_json()
        golf_course = data.get('golfCourse')
        bet_amount = data.get('betAmount')
        players = data.get('players') # List of player names
        editor = data.get('editor')

        if not all([golf_course, bet_amount, players, editor]):
            return https_fn.Response("Missing required fields", status=400)

        game_id = game_service.start_new_game(golf_course, bet_amount, players, editor)

        return https_fn.Response(json.dumps({"gameId": game_id, "message": "Game started successfully!"}), status=200, mimetype="application/json")
    except Exception as e:
        return https_fn.Response(f"Error starting game: {e}", status=500)

def update_score_and_game_status_controller(request: https_fn.Request):
    """Handles the logic for updating score and game status."""
    game_service = GameService() # Instantiate GameService inside the function
    try:
        data = request.get_json()
        game_id = data.get('gameId')
        updated_players_data = data.get('players') # List of updated player objects
        new_status = data.get('status')

        if not all([game_id, updated_players_data]):
            return https_fn.Response("Missing required fields", status=400)

        game_service.update_game_data(game_id, updated_players_data, new_status)

        return https_fn.Response("Score and game status updated successfully!", status=200)
    except Exception as e:
        return https_fn.Response(f"Error updating score and game status: {e}", status=500)

def get_game_list_controller(request: https_fn.Request):
    """Handles the logic for getting the game list."""
    game_service = GameService() # Instantiate GameService inside the function
    try:
        games = game_service.get_all_games_list()
        # Convert datetime objects to string for JSON serialization
        for game in games:
            if 'createdAt' in game and isinstance(game['createdAt'], datetime):
                game['createdAt'] = game['createdAt'].isoformat()
            if 'updatedAt' in game and isinstance(game['updatedAt'], datetime):
                game['updatedAt'] = game['updatedAt'].isoformat()

        return https_fn.Response(json.dumps(games), status=200, mimetype="application/json")
    except Exception as e:
        return https_fn.Response(f"Error getting game list: {e}", status=500)

def delete_game_controller(request: https_fn.Request):
    """Handles the logic for deleting a game."""
    game_service = GameService() # Instantiate GameService inside the function
    try:
        game_id = request.args.get('gameId')
        if not game_id:
            return https_fn.Response("Missing gameId parameter", status=400)

        game_service.delete_existing_game(game_id)

        return https_fn.Response("Game deleted successfully!", status=200)
    except Exception as e:
        return https_fn.Response(f"Error deleting game: {e}", status=500)

def get_game_info_controller(request: https_fn.Request):
    """Handles the logic for getting game info."""
    game_service = GameService() # Instantiate GameService inside the function
    try:
        game_id = request.args.get('gameId')
        if not game_id:
            return https_fn.Response("Missing gameId parameter", status=400)

        game_data = game_service.get_game_details(game_id)

        if not game_data:
            return https_fn.Response("Game not found", status=404)

        # Convert datetime objects to string for JSON serialization
        if 'createdAt' in game_data and isinstance(game_data['createdAt'], datetime.datetime):
            game_data['createdAt'] = game_data['createdAt'].isoformat()
        if 'updatedAt' in game_data and isinstance(game_data['updatedAt'], datetime.datetime):
            game_data['updatedAt'] = game_data['updatedAt'].isoformat()

        return https_fn.Response(json.dumps(game_data), status=200, mimetype="application/json")
    except Exception as e:
        return https_fn.Response(f"Error getting game info: {e}", status=500)
