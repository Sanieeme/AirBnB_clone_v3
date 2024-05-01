#!/usr/bin/python3
"""Views for the reviews objects
"""
from models import storage
from models.review import Review
from models.user import User
from models.place import Place
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/places/<string:place_id>/reviews', strict_slashes=False)
def all_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<string:review_id>')
def get_review(review_id):
    """Retrieves a Review object."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if review is not None:
        review.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/places/<string:place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def post_review(place_id):
    """Creates a Review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    else:
        req = request.get_json()
        user = storage.get(User, req['user_id'])
    if user is None:
        abort(404)
    if 'text' not in req:
        abort(400, 'Missing text')
    req['place_id'] = place_id
    review = Review(**req)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def put_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    req = request.get_json()
    excluded = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, val in req.items():
        if key not in excluded:
            setattr(review, key, val)
    storage.save()
    return jsonify(review.to_dict()), 200
