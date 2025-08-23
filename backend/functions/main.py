from firebase_functions import https_fn
from firebase_admin import initialize_app, credentials
import firebase_admin
import os
from controllers import game_controller, user_controller
from utils.auth_utils import require_auth

# サービスアカウントキーのパスを正しく設定
# Firebase Admin の初期化
if not firebase_admin._apps:  # ←二重初期化を防ぐため
    # 本番かどうかを環境変数で判定（Cloud Functions上なら FIREBASE_CONFIG が必ず入る）
    if os.getenv("FIREBASE_CONFIG") or os.getenv("K_SERVICE"):
        # 本番（GCP/Firebase Functions）はデフォルト認証でOK
        initialize_app()
    else:
        # ローカル開発 → サービスアカウントキーを使う
        cred_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            'olynpicgolf-firebase-adminsdk-114c2-6abf1bf32d.json'
        )
        cred = credentials.Certificate(cred_path)
        initialize_app(cred)

@https_fn.on_request()
def startGame(request: https_fn.Request):
    # CORSプリフライトリクエストの処理
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': 'https://olynpicgolf.web.app',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Max-Age': '3600'
        }
        return https_fn.Response(status=204, headers=headers)

    # 通常のリクエストの処理
    response = game_controller.start_game_controller(request)
    response.headers.set('Access-Control-Allow-Origin', 'https://olynpicgolf.web.app')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.set('Access-Control-Max-Age', '3600')
    return response

@https_fn.on_request()
def updateScoreAndGameStatus(request: https_fn.Request):
    # CORSプリフライトリクエストの処理
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': 'https://olynpicgolf.web.app',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Max-Age': '3600'
        }
        return https_fn.Response(status=204, headers=headers)

    # 通常のリクエストの処理
    response = game_controller.update_score_and_game_status_controller(request)
    response.headers.set('Access-Control-Allow-Origin', 'https://olynpicgolf.web.app')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.set('Access-Control-Max-Age', '3600')
    return response

@https_fn.on_request()
@require_auth
def getGameList(request: https_fn.Request):
    # CORSプリフライトリクエストの処理
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': 'https://olynpicgolf.web.app',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Max-Age': '3600'
        }
        return https_fn.Response(status=204, headers=headers)

    # 通常のリクエストの処理
    response = game_controller.get_game_list_controller(request)
    response.headers.set('Access-Control-Allow-Origin', 'https://olynpicgolf.web.app')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.set('Access-Control-Max-Age', '3600')
    return response

@https_fn.on_request()
def deleteGame(request: https_fn.Request):
    # CORSプリフライトリクエストの処理
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': 'https://olynpicgolf.web.app',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Max-Age': '3600'
        }
        return https_fn.Response(status=204, headers=headers)

    # 通常のリクエストの処理
    response = game_controller.delete_game_controller(request)
    response.headers.set('Access-Control-Allow-Origin', 'https://olynpicgolf.web.app')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.set('Access-Control-Max-Age', '3600')
    return response

@https_fn.on_request()
def getGameInfo(request: https_fn.Request):
    # CORSプリフライトリクエストの処理
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': 'https://olynpicgolf.web.app',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Max-Age': '3600'
        }
        return https_fn.Response(status=204, headers=headers)

    # 通常のリクエストの処理
    response = game_controller.get_game_info_controller(request)
    response.headers.set('Access-Control-Allow-Origin', 'https://olynpicgolf.web.app')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.set('Access-Control-Max-Age', '3600')
    return response

@https_fn.on_request()
@require_auth
def registerOrUpdateUser(request: https_fn.Request):
    # CORSプリフライトリクエストの処理
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': 'https://olynpicgolf.web.app',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Max-Age': '3600'
        }
        return https_fn.Response(status=204, headers=headers)

    # 通常のリクエストの処理
    response = user_controller.register_or_update_user_controller(request)
    response.headers.set('Access-Control-Allow-Origin', 'https://olynpicgolf.web.app')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.set('Access-Control-Max-Age', '3600')
    return response

@https_fn.on_request()
@require_auth
def getUser(request: https_fn.Request):
    # CORSプリフライトリクエストの処理
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': 'https://olynpicgolf.web.app',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Max-Age': '3600'
        }
        return https_fn.Response(status=204, headers=headers)

    # 通常のリクエストの処理
    response = user_controller.get_user_controller(request)
    response.headers.set('Access-Control-Allow-Origin', 'https://olynpicgolf.web.app')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.set('Access-Control-Max-Age', '3600')
    return response

@https_fn.on_request()
@require_auth
def addCompanion(request: https_fn.Request):
    # CORSプリフライトリクエストの処理
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': 'https://olynpicgolf.web.app',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Max-Age': '3600'
        }
        return https_fn.Response(status=204, headers=headers)

    # 通常のリクエストの処理
    response = user_controller.add_companion_controller(request)
    response.headers.set('Access-Control-Allow-Origin', 'https://olynpicgolf.web.app')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.set('Access-Control-Max-Age', '3600')
    return response

@https_fn.on_request()
@require_auth
def getCompanions(request: https_fn.Request):
    # CORSプリフライトリクエストの処理
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': 'https://olynpicgolf.web.app',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Max-Age': '3600'
        }
        return https_fn.Response(status=204, headers=headers)

    # 通常のリクエストの処理
    response = user_controller.get_companions_controller(request)
    response.headers.set('Access-Control-Allow-Origin', 'https://olynpicgolf.web.app')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.set('Access-Control-Max-Age', '3600')
    return response

@https_fn.on_request()
@require_auth
def getCompanion(request: https_fn.Request):
    # CORSプリフライトリクエストの処理
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': 'https://olynpicgolf.web.app',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Max-Age': '3600'
        }
        return https_fn.Response(status=204, headers=headers)

    # 通常のリクエストの処理
    response = user_controller.get_companion_controller(request)
    response.headers.set('Access-Control-Allow-Origin', 'https://olynpicgolf.web.app')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.set('Access-Control-Max-Age', '3600')
    return response

@https_fn.on_request()
@require_auth
def updateCompanion(request: https_fn.Request):
    # CORSプリフライトリクエストの処理
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': 'https://olynpicgolf.web.app',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Max-Age': '3600'
        }
        return https_fn.Response(status=204, headers=headers)

    # 通常のリクエストの処理
    response = user_controller.update_companion_controller(request)
    response.headers.set('Access-Control-Allow-Origin', 'https://olynpicgolf.web.app')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.set('Access-Control-Max-Age', '3600')
    return response

@https_fn.on_request()
@require_auth
def deleteCompanion(request: https_fn.Request):
    # CORSプリフライトリクエストの処理
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': 'https://olynpicgolf.web.app',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Max-Age': '3600'
        }
        return https_fn.Response(status=204, headers=headers)

    # 通常のリクエストの処理
    response = user_controller.delete_companion_controller(request)
    response.headers.set('Access-Control-Allow-Origin', 'https://olynpicgolf.web.app')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.set('Access-Control-Max-Age', '3600')
    return response

@https_fn.on_request()
@require_auth
def submitReview(request: https_fn.Request):
    # CORSプリフライトリクエストの処理
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': 'https://olynpicgolf.web.app',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Max-Age': '3600'
        }
        return https_fn.Response(status=204, headers=headers)

    # 通常のリクエストの処理
    from controllers import review_controller
    response = review_controller.submit_review_controller(request)
    response.headers.set('Access-Control-Allow-Origin', 'https://olynpicgolf.web.app')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.set('Access-Control-Max-Age', '3600')
    return response

@https_fn.on_request()
def getReviews(request: https_fn.Request):
    # CORSプリフライトリクエストの処理
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': 'https://olynpicgolf.web.app',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Max-Age': '3600'
        }
        return https_fn.Response(status=204, headers=headers)

    # 通常のリクエストの処理
    from controllers import review_controller
    response = review_controller.get_reviews_controller(request)
    response.headers.set('Access-Control-Allow-Origin', 'https://olynpicgolf.web.app')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.set('Access-Control-Max-Age', '3600')
    return response