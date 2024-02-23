#!/usr/bin/python3
"""
This module is about the state route of the API
"""
from flask import jsonify, request, abort, make_response
from models import storage
from api.v1.views import app_views


@app_views.route("/states", methods=["GET"])
def get_states():
    """get state information for all states"""
    states = []
    for state in storage.all(storage.CLASSES["State"]).values():
        states.append(state.to_dict())
    return make_response(jsonify(states), 200)


@app_views.route("/states/<string:state_id>", methods=["GET"])
def get_state(state_id):
    """get state information for specified state"""
    state = storage.get(storage.CLASSES["State"], state_id)
    if state is None:
        abort(404)
    return make_response(jsonify(state.to_dict()), 200)


@app_views.route(
    "/states/<string:state_id>",
    methods=["DELETE"],
)
def delete_state(state_id):
    """deletes a state based on its state_id"""
    state = storage.get(storage.CLASSES["State"], state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=["POST"])
def post_state():
    """create a new state"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    state = storage.CLASSES["State"](**request.get_json())
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<string:state_id>", methods=["PUT"])
def put_state(state_id):
    """update a state"""
    state = storage.get(storage.CLASSES["State"], state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for attr, val in request.get_json().items():
        if attr not in ["id", "created_at", "updated_at"]:
            setattr(state, attr, val)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
