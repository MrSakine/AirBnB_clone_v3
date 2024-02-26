#!/usr/bin/python3
"""Place objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place
from models.city import City
from os import getenv
import requests
import json


@app_views.route(
    "/cities/<string:city_id>/places",
    methods=["GET"],
)
def get_places(city_id):
    """get place information for all places in a specified city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return make_response(jsonify(places), 200)


@app_views.route("/places/<string:place_id>", methods=["GET"])
def get_place(place_id):
    """get place information for specified place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route(
    "/places/<string:place_id>",
    methods=["DELETE"],
)
def delete_place(place_id):
    """deletes a place based on its place_id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route(
    "/cities/<string:city_id>/places",
    methods=["POST"],
)
def post_place(city_id):
    """create a new place"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    kwargs = request.get_json()
    if "user_id" not in kwargs:
        abort(400, "Missing user_id")
    user = storage.get("User", kwargs["user_id"])
    if user is None:
        abort(404)
    if "name" not in kwargs:
        abort(400, "Missing name")
    kwargs["city_id"] = city_id
    place = Place(**kwargs)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route("/places/<string:place_id>", methods=["PUT"])
def put_place(place_id):
    """update a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for attr, val in request.get_json().items():
        if attr not in [
            "id",
            "user_id",
            "city_id",
            "created_at",
            "updated_at",
        ]:
            setattr(place, attr, val)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route("/places_search", methods=["POST"])
def places_search():
    """
    places route to handle http method for request to search places
    """
    if not request.is_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    dic = request.get_json()
    all_places = storage.all(Place).values()
    places = []
    states = dic.get("states")
    cities = dic.get("cities")
    amenities = dic.get("amenities")
    if amenities and len(amenities) != 0:
        for place in all_places:
            ids = [o.id for o in place.amenities]
            if all(id in ids for id in amenities):
                del place.amenities
                places.append(place)
    else:
        places = all_places
    all_places, places = places, []
    if cities and len(cities) != 0:
        for place in all_places:
            if place.city_id in cities:
                places.append(place)
    else:
        places = all_places
    all_places, places = places, []

    if states and len(states) != 0:
        for place in all_places:
            city = storage.get(City, place.city_id)
            if city.state_id in states:
                places.append(place)
    else:
        places = all_places
    all_places, places = places, []

    for place in all_places:
        places.append(place.to_dict())

    return make_response(jsonify(places), 200)
