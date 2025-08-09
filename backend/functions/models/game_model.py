from firebase_admin import firestore
import datetime

db = firestore.client()

class GameModel:
    def __init__(self):
        self.collection = db.collection("games")

    def create_game(self, game_id, game_data):
        game_data["createdAt"] = datetime.datetime.now(datetime.timezone.utc)
        game_data["updatedAt"] = datetime.datetime.now(datetime.timezone.utc)
        self.collection.document(game_id).set(game_data)

    def get_game(self, game_id):
        doc = self.collection.document(game_id).get()
        if doc.exists:
            return doc.to_dict()
        return None

    def update_game(self, game_id, updates):
        updates["updatedAt"] = datetime.datetime.now(datetime.timezone.utc)
        self.collection.document(game_id).update(updates)

    def delete_game(self, game_id):
        self.collection.document(game_id).delete()

    def get_all_games(self):
        docs = self.collection.stream()
        games = []
        for doc in docs:
            games.append(doc.to_dict())
        return games
