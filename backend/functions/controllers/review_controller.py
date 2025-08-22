from firebase_functions import https_fn
from services import review_service
from utils.auth_utils import get_user_id_from_request
from utils.helpers import cors_enabled
import json

@cors_enabled
def submit_review_controller(request: https_fn.Request):
    if request.method != 'POST':
        return https_fn.Response("Method Not Allowed", status=405)

    try:
        user_id = get_user_id_from_request(request)
        if not user_id:
            return https_fn.Response("Unauthorized", status=401)

        request_json = request.get_json(silent=True)
        if not request_json:
            return https_fn.Response("Invalid JSON", status=400)

        rating = request_json.get('rating')
        comment = request_json.get('comment', '')
        user_name = request_json.get('userName', '匿名ユーザー') # Get userName from request

        if not rating:
            return https_fn.Response("Rating is required", status=400)

        review_id = review_service.add_review(user_id, user_name, rating, comment)
        return https_fn.Response(json.dumps({"message": "Review submitted successfully", "reviewId": review_id}),
                                 headers={"Content-Type": "application/json"}, status=200)
    except Exception as e:
        print(f"Error submitting review: {e}")
        return https_fn.Response(json.dumps({"error": str(e)}), headers={"Content-Type": "application/json"}, status=500)

@cors_enabled
def get_reviews_controller(request: https_fn.Request):
    if request.method != 'GET':
        return https_fn.Response("Method Not Allowed", status=405)

    try:
        reviews = review_service.get_all_reviews()
        return https_fn.Response(json.dumps({"reviews": reviews}),
                                 headers={"Content-Type": "application/json"}, status=200)
    except Exception as e:
        print(f"Error getting reviews: {e}")
        return https_fn.Response(json.dumps({"error": str(e)}), headers={"Content-Type": "application/json"}, status=500)
