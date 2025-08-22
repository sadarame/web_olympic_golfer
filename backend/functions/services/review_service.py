from firebase_admin import firestore
from datetime import datetime

db = firestore.client()

def add_review(user_id, user_name, rating, comment):
    review_ref = db.collection('reviews').document()
    review_data = {
        'userId': user_id,
        'userName': user_name,
        'rating': int(rating),
        'comment': comment,
        'createdAt': datetime.now().isoformat(),
    }
    review_ref.set(review_data)
    return review_ref.id

def get_all_reviews():
    reviews_ref = db.collection('reviews').order_by('createdAt', direction=firestore.Query.DESCENDING).stream()
    reviews = []
    for review in reviews_ref:
        review_data = review.to_dict()
        reviews.append({
            'id': review.id,
            'userId': review_data.get('userId'),
            'userName': review_data.get('userName'),
            'rating': review_data.get('rating'),
            'comment': review_data.get('comment'),
            'createdAt': review_data.get('createdAt'),
        })
    return reviews
