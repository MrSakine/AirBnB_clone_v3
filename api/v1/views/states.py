#!/usr/bin/python3
"""
This module is about the state route of the API
"""
from flask import jsonify, request, abort, make_response
from models import storage, CLASSES
from api.v1.views import app_views


@app_views.route("/states", methods=["GET", "POST"])
def states():
    """Get all states"""
    if request.method == "GET":
        return jsonify(
            [
                state.to_dict()
                for state in storage.all("State").values()
            ]
        )
    if request.method == "POST":
        if not request.get_json():
            return make_response(
                jsonify({"error": "Not a JSON"}), 400
            )
        if "name" not in request.get_json():
            return make_response(
                jsonify({"error": "Missing name"}), 400
            )
        new_state = CLASSES["State"](**request.get_json())
        new_state.save()
        return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route(
    "/states/<state_id>", methods=["GET", "DELETE", "PUT"]
)
def get_state(state_id=None):
    """Get a specified state"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    if request.method == "GET":
        return make_response(jsonify(state.to_dict()), 200)
    if request.method == "DELETE":
        state.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    if request.method == "PUT":
        if not request.get_json():
            return make_response(
                jsonify({"error": "Not a JSON"}), 400
            )
        for key, value in request.get_json().items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(state, key, value)
        state.save()
        return make_response(jsonify(state.to_dict()), 200)
