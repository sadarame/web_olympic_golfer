

import json
import os
from unittest.mock import Mock
from controllers.game_controller import start_game_controller
from firebase_admin import initialize_app, credentials

# --- モックデータ ---
# 実際のテストシナリオに合わせてこのデータを変更してください
mock_data = {
    "golfCourse": "Test Course",
    "betAmount": 100,
    "players": ["Player 1", "Player 2"],
    "editor": "Editor Name"
}

# --- リクエストオブジェクトのモックを作成 ---
# firebase_functions.https_fn.Requestオブジェクトを模倣します
mock_request = Mock()
mock_request.get_json.return_value = mock_data
mock_request.args = {} # GETリクエストのクエリパラメータ用

# --- Firebaseアプリの初期化 ---
# GOOGLE_APPLICATION_CREDENTIALS 環境変数からサービスアカウントキーを読み込みます
if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
    cred = credentials.Certificate(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
    initialize_app(cred)
else:
    print("WARNING: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
    print("Firebase app will be initialized without credentials, which may cause issues with Firestore access.")
    initialize_app() # 資格情報なしで初期化（テスト目的の場合など）

# --- テスト対象の関数を呼び出し ---
if __name__ == "__main__":
    print("Running start_game_controller locally...")
    
    response = start_game_controller(mock_request)
    
    print("\n--- Response ---")
    print(f"Status Code: {response.status_code}")
    print(f"Mimetype: {response.mimetype}")
    print(f"Body: {response.get_data(as_text=True)}")
    print("----------------")


