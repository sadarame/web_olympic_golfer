from models.game_model import GameModel
import uuid

class GameService:
    def __init__(self):
        self.game_model = GameModel()

    def start_new_game(self, game_id, golf_course, bet_amount, players, editor, memo): # Add memo
        initial_players_data = []
        for player_name in players:
            initial_players_data.append({
                "name": player_name,
                "score": None,
                "bonusPoints": 0,
                "totalPoints": 0
            })

        game_data = {
            "gameId": game_id,
            "golfCourse": golf_course,
            "betAmount": bet_amount,
            "editor": editor,
            "players": initial_players_data,
            "status": "in_progress",
            "memo": memo # Add memo to game_data
        }
        self.game_model.create_game(game_id, game_data)

    def update_game_data(self, game_id, updated_players_data, new_status=None):
        updates = {"players": updated_players_data}
        if new_status:
            updates["status"] = new_status
        self.game_model.update_game(game_id, updates)

    def get_game_details(self, game_id):
        return self.game_model.get_game(game_id)

    def get_all_games_list(self):
        return self.game_model.get_all_games()

    def delete_existing_game(self, game_id):
        self.game_model.delete_game(game_id)

    # TODO: ポイント計算ロジックをここに追加
    def calculate_points(self, game_data):
        # この関数でスコアに基づいてポイントを計算し、game_dataのplayersを更新する
        # 例: game_data["players"][0]["totalPoints"] = ...
        return game_data