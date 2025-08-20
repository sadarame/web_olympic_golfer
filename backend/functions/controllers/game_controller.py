# This file will contain the business logic for game-related endpoints.
from services.game_service import GameService
import json
from datetime import datetime
from firebase_functions import https_fn
from utils.helpers import cors_enabled
from utils.auth_utils import get_user_from_request

@cors_enabled
def start_game_controller(request: https_fn.Request):
    """Handles the logic for starting a new game."""
    game_service = GameService() # Instantiate GameService inside the function
    try:
        data = request.get_json()
        print(f"Received data: {data}") # Add this line for debugging

        game_id = data.get('gameId')
        golf_course = data.get('golfCourse')
        bet_amount = data.get('betAmount')
        players = data.get('players')
        editor = data.get('editor')
        memo = data.get('memo') # Add memo

        print(f"game_id: {game_id}, type: {type(game_id)}")
        print(f"golf_course: {golf_course}, type: {type(golf_course)}")
        print(f"bet_amount: {bet_amount}, type: {type(bet_amount)}")
        print(f"players: {players}, type: {type(players)}")
        print(f"editor: {editor}, type: {type(editor)}")
        print(f"memo: {memo}, type: {type(memo)}") # Print memo for debugging


        if not all([game_id, golf_course, bet_amount, players, editor]): # memoのチェックを外す
            return https_fn.Response("Missing required fields", status=400)

        game_service.start_new_game(game_id, golf_course, bet_amount, players, editor, memo) # Pass memo

        headers = {'Content-Type': 'application/json'}
        return https_fn.Response(json.dumps({"message": "Game started successfully!"}), status=200, headers=headers)
    except Exception as e:
        return https_fn.Response(f"Error starting game: {e}", status=500)

@cors_enabled
def update_score_and_game_status_controller(request: https_fn.Request):
    """Handles the logic for updating score and game status."""
    game_service = GameService()
    try:
        data = request.get_json()
        game_id = data.get('gameId')
        updated_players_data = data.get('players')
        new_status = data.get('status')

        if not all([game_id, updated_players_data, new_status]):
            return https_fn.Response("Missing required fields", status=400)

        game_service.update_game_data(game_id, updated_players_data, new_status)

        headers = {'Content-Type': 'application/json'}
        return https_fn.Response(json.dumps({"message": "Score and game status updated successfully!"}), status=200, headers=headers)
    except Exception as e:
        return https_fn.Response(f"Error updating score and game status: {e}", status=500)

@cors_enabled
def get_game_list_controller(request: https_fn.Request):
    """Handles the logic for getting the game list for the authenticated user."""
    game_service = GameService()
    try:
        decoded_token = get_user_from_request(request)
        if not decoded_token or not decoded_token.get('sub'):
            return https_fn.Response("Unauthorized", status=401)
        
        user_id = decoded_token['sub']
        games = game_service.get_games_by_editor(user_id)
        
        # Convert datetime objects to string for JSON serialization
        for game in games:
            if 'createdAt' in game and isinstance(game['createdAt'], datetime):
                game['createdAt'] = game['createdAt'].isoformat()
            if 'updatedAt' in game and isinstance(game['updatedAt'], datetime):
                game['updatedAt'] = game['updatedAt'].isoformat()

        return https_fn.Response(json.dumps(games), status=200, mimetype="application/json")
    
    except Exception as e:
        print(f"Error in get_game_list_controller: {e}")
        return https_fn.Response(f"Error getting game list: {e}", status=500)

@cors_enabled
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

@cors_enabled
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
