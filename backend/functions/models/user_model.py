from firebase_admin import firestore
import datetime

class UserModel:
    def __init__(self):
        self.collection = self._get_db().collection("users")

    def _get_db(self):
        return firestore.client()

    def create_user(self, user_id, user_data):
        """ユーザーを作成する"""
        user_data["createdAt"] = datetime.datetime.now(datetime.timezone.utc)
        user_data["updatedAt"] = datetime.datetime.now(datetime.timezone.utc)
        self.collection.document(user_id).set(user_data)

    def get_user(self, user_id):
        """ユーザー情報を取得する"""
        doc = self.collection.document(user_id).get()
        if doc.exists:
            return doc.to_dict()
        return None

    def update_user(self, user_id, updates):
        """ユーザー情報を更新する"""
        updates["updatedAt"] = datetime.datetime.now(datetime.timezone.utc)
        self.collection.document(user_id).update(updates)

    def upsert_user(self, user_id, user_data):
        """ユーザー情報を作成または更新する（upsert）"""
        user_data["updatedAt"] = datetime.datetime.now(datetime.timezone.utc)
        doc_ref = self.collection.document(user_id)
        doc = doc_ref.get()
        
        if doc.exists:
            # 既存ユーザーの場合、createdAtは保持
            existing_data = doc.to_dict()
            user_data["createdAt"] = existing_data.get("createdAt", user_data["updatedAt"])
            doc_ref.update(user_data)
        else:
            # 新規ユーザーの場合、createdAtを設定
            user_data["createdAt"] = user_data["updatedAt"]
            doc_ref.set(user_data)

    def delete_user(self, user_id):
        """ユーザーを削除する"""
        self.collection.document(user_id).delete()
