#!/usr/bin/python3
"""Review object that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review


@app_views.route("/places/<string:place_id>/reviews", methods=["GET"])
def get_reviews(place_id):
    """get reviews for a specified place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return make_response(jsonify(reviews), 200)


@app_views.route("/reviews/<string:review_id>", methods=["GET"])
def get_review(review_id):
    """get review information for specified review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return make_response(jsonify(review.to_dict()), 200)


@app_views.route("/reviews/<string:review_id>", methods=["DELETE"])
def delete_review(review_id):
    """deletes a review based on its review_id"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route(
    "/places/<string:place_id>/reviews", methods=["POST"]
)
def post_review(place_id):
    """create a new review"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    kwargs = request.get_json()
    if "user_id" not in kwargs:
        abort(400, "Missing user_id")
    user = storage.get("User", kwargs["user_id"])
    if user is None:
        abort(404)
    if "text" not in kwargs:
        abort(400, "Missing text")
    kwargs["place_id"] = place_id
    review = Review(**kwargs)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route("/reviews/<string:review_id>", methods=["PUT"])
def put_review(review_id):
    """update a review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for attr, val in request.get_json().items():
        if attr not in [
            "id",
            "user_id",
            "place_id",
            "created_at",
            "updated_at",
        ]:
            setattr(review, attr, val)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
