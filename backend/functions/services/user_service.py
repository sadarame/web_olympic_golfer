from models.user_model import UserModel

class UserService:
    def __init__(self):
        self.user_model = UserModel()

    def register_or_update_user(self, user_id, user_info, custom_name):
        """
        ユーザー情報を登録または更新する
        
        Args:
            user_id (str): ユーザーの一意なID (Googleのsub)
            user_info (dict): ユーザー情報
            custom_name (str): ユーザーが設定した名前
            
        Returns:
            dict: 登録・更新されたユーザー情報
        """
        # ユーザーIDで既存ユーザーを検索
        existing_user = self.user_model.get_user(user_id)
        
        # ユーザーデータを準備
        user_data = {
            "userId": user_id,
            "customName": custom_name,
            "userInfo": user_info,
        }
        
        # ユーザー情報をupsert（作成または更新）
        self.user_model.upsert_user(user_id, user_data)
        
        # 更新されたユーザー情報を返す
        return self.user_model.get_user(user_id)

    def get_user_by_id(self, user_id):
        """
        ユーザーIDでユーザー情報を取得する
        
        Args:
            user_id (str): ユーザーID
            
        Returns:
            dict: ユーザー情報（存在しない場合はNone）
        """
        return self.user_model.get_user(user_id)

    def add_companion(self, user_id, name):
        """
        同伴者を追加する
        
        Args:
            user_id (str): ユーザーID
            name (str): 同伴者の名前
            
        Returns:
            dict: 追加された同伴者の情報
        """
        return self.user_model.add_companion(user_id, name)

    def delete_user(self, user_id):
        """
        ユーザーを削除する
        
        Args:
            user_id (str): ユーザーID
        """
        self.user_model.delete_user(user_id)
