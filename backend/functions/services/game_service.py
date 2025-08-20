from models.game_model import GameModel
import uuid

class GameService:
    def __init__(self):
        self.game_model = GameModel()

    def start_new_game(self, game_id, golf_course, bet_amount, players, editor, memo):
        initial_players_data = []
        for player in players:
            initial_players_data.append({
                "id": player.get('id'),
                "name": player.get('name'),
                "points": 0,
                "amount": 0
            })

        game_data = {
            "gameId": game_id,
            "golfCourse": golf_course,
            "betAmount": bet_amount,
            "editor": editor,
            "players": initial_players_data,
            "status": "in_progress",
            "memo": memo,
            "editorResultAmount": 0 # Initialize the field
        }
        self.game_model.create_game(game_id, game_data)

    def update_game_data(self, game_id, updated_players_data, new_status=None):
        updates = {"players": updated_players_data}
        
        if new_status:
            updates["status"] = new_status

        # If the game is being completed, find the editor's result and save it.
        if new_status == "completed":
            game_doc = self.game_model.get_game(game_id)
            if game_doc:
                editor_id = game_doc.get("editor")
                editor_result_amount = 0 # Default to 0

                if editor_id and updated_players_data:
                    for player in updated_players_data:
                        if player.get("id") == editor_id:
                            editor_result_amount = player.get("amount", 0)
                            break
                
                updates["editorResultAmount"] = editor_result_amount

        self.game_model.update_game(game_id, updates)

    def get_game_details(self, game_id):
        return self.game_model.get_game(game_id)

    def get_all_games_list(self):
        return self.game_model.get_all_games()

    def get_games_by_editor(self, editor_id):
        return self.game_model.get_games_by_editor(editor_id)

    def delete_existing_game(self, game_id):
        self.game_model.delete_game(game_id)

    # TODO: ポイント計算ロジックをここに追加
    def calculate_points(self, game_data):
        # この関数でスコアに基づいてポイントを計算し、game_dataのplayersを更新する
        # 例: game_data["players"][0]["totalPoints"] = ...
        return game_data
