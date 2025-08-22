from firebase_admin import firestore

class ReviewService:
    def __init__(self):
        self.db = firestore.client()

    def add_review(self, user_id, user_name, rating, comment):
        review_ref = self.db.collection('reviews').document()
        review_data = {
            'userId': user_id,
            'userName': user_name,
            'rating': int(rating),
            'comment': comment,
        }
        review_ref.set(review_data)
        return review_ref.id

    def get_all_reviews(self):
        reviews_ref = self.db.collection('reviews').stream()
        reviews = []
        for review in reviews_ref:
            review_data = review.to_dict()
            reviews.append({
                'id': review.id,
                'userId': review_data.get('userId'),
                'userName': review_data.get('userName'),
                'rating': review_data.get('rating'),
                'comment': review_data.get('comment'),
            })
        return reviews
