from firebase_functions import https_fn
from services.review_service import ReviewService
from utils.auth_utils import get_user_from_request
import json

def submit_review_controller(request: https_fn.Request):
    review_service = ReviewService()

    if request.method == 'OPTIONS':
        return https_fn.Response(
            status=200,
            headers={
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            }
        )

    if request.method != 'POST':
        return https_fn.Response("Method Not Allowed", status=405, headers={'Access-Control-Allow-Origin': '*'})

    try:
        decoded_token = get_user_from_request(request)
        if not decoded_token or not decoded_token.get('sub'):
            return https_fn.Response("Unauthorized", status=401, headers={'Access-Control-Allow-Origin': '*'})
        
        user_id = decoded_token['sub']

        request_json = request.get_json(silent=True)
        if not request_json:
            return https_fn.Response("Invalid JSON", status=400, headers={'Access-Control-Allow-Origin': '*'})

        rating = request_json.get('rating')
        comment = request_json.get('comment', '')
        user_name = request_json.get('userName', '匿名ユーザー')

        if not rating:
            return https_fn.Response("Rating is required", status=400, headers={'Access-Control-Allow-Origin': '*'})

        review_id = review_service.add_review(user_id, user_name, rating, comment)
        return https_fn.Response(json.dumps({"message": "Review submitted successfully", "reviewId": review_id}),
                                 headers={"Content-Type": "application/json", 'Access-Control-Allow-Origin': '*'}, status=200)
    except Exception as e:
        print(f"Error submitting review: {e}")
        return https_fn.Response(json.dumps({"error": str(e)}), headers={"Content-Type": "application/json", 'Access-Control-Allow-Origin': '*'}, status=500)

def get_reviews_controller(request: https_fn.Request):
    review_service = ReviewService()

    if request.method == 'OPTIONS':
        return https_fn.Response(
            status=200,
            headers={
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            }
        )

    if request.method != 'GET':
        return https_fn.Response("Method Not Allowed", status=405, headers={'Access-Control-Allow-Origin': '*'})

    try:
        reviews = review_service.get_all_reviews()
        return https_fn.Response(json.dumps({"reviews": reviews}),
                                 headers={"Content-Type": "application/json", 'Access-Control-Allow-Origin': '*'}, status=200)
    except Exception as e:
        print(f"Error getting reviews: {e}")
        return https_fn.Response(json.dumps({"error": str(e)}), headers={"Content-Type": "application/json", 'Access-Control-Allow-Origin': '*'}, status=500)
