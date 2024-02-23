#!/usr/bin/python3
"""User object that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"])
def get_users():
    """method that gets user info for all users"""
    users = []
    for user in storage.all("User").values():
        users.append(user.to_dict())
    return make_response(jsonify(users), 200)


@app_views.route("/users/<string:user_id>", methods=["GET"])
def get_user(user_id):
    """method that gets a user"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return make_response(jsonify(user.to_dict()), 200)


@app_views.route(
    "/users/<string:user_id>",
    methods=["DELETE"],
)
def delete_user(user_id):
    """method that deletes a user based on user_id"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=["POST"])
def post_user():
    """method that create User"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "email" not in request.get_json():
        abort(400, "Missing email")
    if "password" not in request.get_json():
        abort(400, "Missing password")
    user = User(**request.get_json())
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route("/users/<string:user_id>", methods=["PUT"])
def put_user(user_id):
    """method that Updates User"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for attr, val in request.get_json().items():
        if attr not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, attr, val)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
