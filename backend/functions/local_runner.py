import json
import os
from unittest.mock import Mock
from controllers.game_controller import start_game_controller
from firebase_admin import initialize_app, credentials

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/yosuke/Desktop/PJ/olympic_golfer/backend/olynpicgolf-firebase-adminsdk-114c2-6abf1bf32d.json"

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
cred = credentials.Certificate(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
initialize_app(cred)

# --- テスト対象の関数を呼び出し ---
if __name__ == "__main__":
    print("Running start_game_controller locally...")
    
    response = start_game_controller(mock_request)
    
    print("\n--- Response ---")
    print(f"Status Code: {response.status_code}")
    print(f"Mimetype: {response.mimetype}")
    print(f"Body: {response.get_data(as_text=True)}")
    print("----------------")