#!/usr/bin/python3
"""
This module is about the state route of the API
"""
from flask import jsonify, request, abort, make_response
from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City


@app_views.route("/states", methods=["GET"])
def get_states():
    """method that gets all states"""
    states = [
        state.to_dict() for state in storage.all(State).values()
    ]
    return jsonify(states)


@app_views.route("/states/<state_id>", methods=["GET"])
def get_state(state_id):
    """method that gets state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states", methods=["POST"])
def create_state():
    """method that creates state"""
    if not request.json:
        abort(400, "Not a JSON")
    if "name" not in request.json:
        abort(400, "Missing name")
    data = request.get_json()
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """method that updates state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """method that deletes state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    associated_cities = storage.all(City).values()
    associated_cities = [
        city
        for city in associated_cities
        if city.state_id == state_id
    ]

    if associated_cities:
        for city in associated_cities:
            city.delete()
            storage.save()

    state.delete()
    storage.save()

    return jsonify({}), 200
