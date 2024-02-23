#!/usr/bin/python3
"""

"""

from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from flasgger import Swagger, swag_from
from models import storage, CLASSES


@app_views.route("/states", methods=["GET", "POST"])
@swag_from(
    "swagger_yaml/states/no_id_states.yml", methods=["GET", "POST"]
)
def no_id_states():
    """ """
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
@swag_from(
    "swagger_yaml/states/id_sates.yml",
    methods=["GET", "DELETE", "PUT"],
)
def id_states(state_id=None):
    """ """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    if request.method == "GET":
        return jsonify(state.to_dict())
    if request.method == "DELETE":
        state.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        if not request.get_json():
            return make_response(
                jsonify({"error": "Not a JSON"}), 400
            )
        for key, value in request.get_json().items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict())
