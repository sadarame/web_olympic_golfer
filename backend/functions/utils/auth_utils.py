import jwt
from functools import wraps
from firebase_admin import auth
from firebase_functions import https_fn
import json
from google.oauth2 import id_token
from google.auth.transport import requests

# フロントエンドのGoogleログインで使用しているクライアントID
GOOGLE_CLIENT_ID = "662503012810-fh86an6fbiu8bm34mrh4kuu98u3c3i1q.apps.googleusercontent.com"

def verify_token(token):
    """
    Firebase IDトークンを検証する
    
    Args:
        token (str): Firebase IDトークン
        
    Returns:
        dict: 検証されたユーザー情報
        None: トークンが無効な場合
    """
    try:
        # Firebase Admin SDKを使ってトークンを検証
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        print(f"Firebase token verification failed: {e}")
        return None

def require_auth(func):
    """
    認証が必要なエンドポイント用のデコレータ
    
    Args:
        func: デコレートする関数
        
    Returns:
        function: 認証チェック付きの関数
    """
    @wraps(func)
    def wrapper(request: https_fn.Request):
        # CORS プリフライトリクエストの場合は、認証をスキップして OPTIONS 応答を返す
        if request.method == 'OPTIONS':
            return func(request)
            
        try:
            # Authorization ヘッダーからトークンを取得
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return https_fn.Response(
                    json.dumps({
                        "error": "Unauthorized",
                        "message": "Authorization header is required"
                    }),
                    status=401,
                    mimetype="application/json",
                    headers={'Access-Control-Allow-Origin': '*'}
                )
            
            # Bearer トークンの形式をチェック
            if not auth_header.startswith('Bearer '):
                return https_fn.Response(
                    json.dumps({
                        "error": "Unauthorized",
                        "message": "Invalid authorization format. Use 'Bearer <token>'"
                    }),
                    status=401,
                    mimetype="application/json",
                    headers={'Access-Control-Allow-Origin': '*'}
                )
            
            # トークンを抽出
            token = auth_header.split(' ')[1]
            
            # トークンを検証
            decoded_token = verify_token(token)
            if not decoded_token:
                return https_fn.Response(
                    json.dumps({
                        "error": "Unauthorized",
                        "message": "Invalid or expired token"
                    }),
                    status=401,
                    mimetype="application/json",
                    headers={'Access-Control-Allow-Origin': '*'}
                )
            
            # リクエストにユーザー情報を追加
            request.user = decoded_token
            
            # 元の関数を実行
            return func(request)
            
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
    
    return wrapper

def get_user_from_request(request: https_fn.Request):
    """
    リクエストからユーザー情報を取得する
    
    Args:
        request: HTTP リクエスト
        
    Returns:
        dict: ユーザー情報（uid, email等）
        None: ユーザー情報が存在しない場合
    """
    return getattr(request, 'user', None)


def get_user_id_from_request(request: https_fn.Request):
    """リクエストからユーザーIDを取得するヘルパー関数"""
    # If request has been processed by require_auth, user info is already attached
    user = get_user_from_request(request)
    if user and (user.get('sub') or user.get('uid')):
        return user.get('sub') or user.get('uid')

    # Fallback: manually parse the Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None

    token = auth_header.split(' ')[1]
    decoded_token = verify_token(token)
    if not decoded_token:
        return None

    return decoded_token.get('sub') or decoded_token.get('uid')

