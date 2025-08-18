from services.user_service import UserService
from utils.auth_utils import get_user_from_request
import json
from datetime import datetime
from firebase_functions import https_fn

def register_or_update_user_controller(request: https_fn.Request):
    """
    ユーザー情報を登録または更新するエンドポイント
    リクエストボディ:
    {
        "userInfo": {
            "name": "string",
            "email": "string",
            "profile": "object"
        },
        "customName": "string"
    }
    """
    user_service = UserService()
    
    try:
        # CORSプリフライトリクエストの処理
        if request.method == 'OPTIONS':
            return https_fn.Response(
                status=200,
                headers={
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, PUT, GET, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
                }
            )

        # 認証済みユーザー情報を取得
        decoded_token = get_user_from_request(request)
        if not decoded_token or not decoded_token.get('sub'):
            return https_fn.Response("Unauthorized", status=401, headers={'Access-Control-Allow-Origin': '*'})
        
        user_id = decoded_token['sub']
        
        data = request.get_json()
        
        # 必須フィールドの検証
        required_fields = ['userInfo', 'customName']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return https_fn.Response(
                json.dumps({
                    "error": "Missing required fields",
                    "missingFields": missing_fields
                }),
                status=400,
                mimetype="application/json",
                headers={'Access-Control-Allow-Origin': '*'}
            )
        
        # ユーザー情報の登録・更新
        user_data = user_service.register_or_update_user(
            user_id=user_id,
            user_info=data['userInfo'],
            custom_name=data['customName']
        )
        
        print(f"User data returned from service: {user_data}") # <--- 追加

        # レスポンスの準備
        response_data = {
            "success": True,
            "message": "User registered/updated successfully",
            "user": user_data
        }
        
        return https_fn.Response(
            json.dumps(response_data, default=str),
            status=200,
            mimetype="application/json",
            headers={'Access-Control-Allow-Origin': '*'}
        )
        
    except Exception as e:
        return https_fn.Response(
            json.dumps({
                "error": "Internal server error",
                "message": str(e)
            }),
            status=500,
            mimetype="application/json",
            headers={'Access-Control-Allow-Origin': '*'}
        )

def get_user_controller(request: https_fn.Request):
    """
    ユーザー情報を取得するエンドポイント
    """
    user_service = UserService()
    
    try:
        # CORSプリフライトリクエストの処理
        if request.method == 'OPTIONS':
            return https_fn.Response(
                status=200,
                headers={
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
                }
            )

        # 認証済みユーザー情報を取得
        decoded_token = get_user_from_request(request)
        if not decoded_token or not decoded_token.get('sub'):
            return https_fn.Response("Unauthorized", status=401, headers={'Access-Control-Allow-Origin': '*'})
        
        user_id = decoded_token['sub']

        # ユーザー情報を取得
        user_data = user_service.get_user_by_id(user_id)
        
        if not user_data:
            return https_fn.Response(
                json.dumps({
                    "error": "User not found",
                    "message": f"No user found with id: {user_id}"
                }),
                status=404,
                mimetype="application/json",
                headers={'Access-Control-Allow-Origin': '*'}
            )
        
        # レスポンスの準備
        response_data = {
            "success": True,
            "user": user_data
        }
        
        return https_fn.Response(
            json.dumps(response_data, default=str),
            status=200,
            mimetype="application/json",
            headers={'Access-Control-Allow-Origin': '*'}
        )
        
    except Exception as e:
        return https_fn.Response(
            json.dumps({
                "error": "Internal server error",
                "message": str(e)
            }),
            status=500,
            mimetype="application/json",
            headers={'Access-Control-Allow-Origin': '*'}
        )

def add_companion_controller(request: https_fn.Request):
    """
    同伴者を追加するエンドポイント
    """
    user_service = UserService()

    try:
        # CORSプリフライトリクエストの処理
        if request.method == 'OPTIONS':
            return https_fn.Response(
                status=200,
                headers={
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
                }
            )

        # 認証済みユーザー情報を取得
        decoded_token = get_user_from_request(request)
        if not decoded_token or not decoded_token.get('sub'):
            return https_fn.Response("Unauthorized", status=401, headers={'Access-Control-Allow-Origin': '*'})
        
        user_id = decoded_token['sub']
        
        data = request.get_json()
        
        # 必須フィールドの検証
        if not data or 'name' not in data or not data['name'].strip():
            return https_fn.Response(
                json.dumps({"error": "Companion name is required"}),
                status=400,
                mimetype="application/json",
                headers={'Access-Control-Allow-Origin': '*'}
            )
        
        name = data['name'].strip()

        # 同伴者の追加
        new_companion = user_service.add_companion(user_id, name)
        
        # レスポンスの準備
        response_data = {
            "success": True,
            "message": "Companion added successfully",
            "companion": new_companion
        }
        
        return https_fn.Response(
            json.dumps(response_data, default=str),
            status=201,
            mimetype="application/json",
            headers={'Access-Control-Allow-Origin': '*'}
        )
        
    except Exception as e:
        return https_fn.Response(
            json.dumps({
                "error": "Internal server error",
                "message": str(e)
            }),
            status=500,
            mimetype="application/json",
            headers={'Access-Control-Allow-Origin': '*'}
        )
