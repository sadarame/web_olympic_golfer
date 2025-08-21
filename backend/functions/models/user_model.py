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

    def add_companion(self, user_id, name, gender=None, relationship=None, memo=None):
        """同伴者をサブコレクションに追加する"""
        user_doc_ref = self.collection.document(user_id)
        user_doc = user_doc_ref.get()

        if not user_doc.exists:
            raise Exception(f"User with ID {user_id} does not exist.")

        # --- 重複チェックの追加 ---
        companions_ref = user_doc_ref.collection("companions")
        existing_companions = companions_ref.where("name", "==", name).limit(1).get()
        if len(existing_companions) > 0:
            raise Exception(f"Companion with name '{name}' already exists for user {user_id}.")
        # --- ここまで追加 ---

        companion_data = {
            "name": name,
            "createdAt": datetime.datetime.now(datetime.timezone.utc),
            "gender": gender,
            "relationship": relationship,
            "memo": memo
        }
        companions_ref = user_doc_ref.collection("companions")
        update_time, companion_ref = companions_ref.add(companion_data)
        return {
            "id": companion_ref.id,
            "name": name,
            "gender": gender,
            "relationship": relationship,
            "memo": memo
        }

    def get_companions(self, user_id):
        """同伴者リストを取得する"""
        companions_ref = self.collection.document(user_id).collection("companions")
        companions = []
        for doc in companions_ref.stream():
            companion_data = doc.to_dict()
            companion_data["id"] = doc.id
            companions.append(companion_data)
        return companions

    def delete_companion(self, user_id, companion_id):
        """同伴者をサブコレクションから削除する"""
        self.collection.document(user_id).collection("companions").document(companion_id).delete()

    def update_companion(self, user_id, companion_id, name, gender=None, relationship=None, memo=None):
        """同伴者の名前を更新する"""
        companion_ref = self.collection.document(user_id).collection("companions").document(companion_id)
        updates = {"name": name}
        if gender is not None:
            updates["gender"] = gender
        if relationship is not None:
            updates["relationship"] = relationship
        if memo is not None:
            updates["memo"] = memo
        companion_ref.update(updates)
        updated_doc = companion_ref.get()
        if updated_doc.exists:
            updated_data = updated_doc.to_dict()
            updated_data["id"] = updated_doc.id
            return updated_data
        return None

    def get_companion(self, user_id, companion_id):
        """特定の同伴者を取得する"""
        doc = self.collection.document(user_id).collection("companions").document(companion_id).get()
        if doc.exists:
            companion_data = doc.to_dict()
            companion_data["id"] = doc.id
            return companion_data
        return None
