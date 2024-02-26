#!/usr/bin/python3
"""Place objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place
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
    all_places = [p for p in storage.all("Place").values()]
    req_json = request.get_json()
    if req_json is None:
        abort(400, "Not a JSON")
    states = req_json.get("states")
    if states and len(states) > 0:
        all_cities = storage.all("City")
        state_cities = set(
            [
                city.id
                for city in all_cities.values()
                if city.state_id in states
            ]
        )
    else:
        state_cities = set()
    cities = req_json.get("cities")
    if cities and len(cities) > 0:
        cities = set(
            [c_id for c_id in cities if storage.get("City", c_id)]
        )
        state_cities = state_cities.union(cities)
    amenities = req_json.get("amenities")
    if len(state_cities) > 0:
        all_places = [
            p for p in all_places if p.city_id in state_cities
        ]
    elif amenities is None or len(amenities) == 0:
        result = [place.to_json() for place in all_places]
        return jsonify(result)
    places_amenities = []
    if amenities and len(amenities) > 0:
        amenities = set(
            [
                a_id
                for a_id in amenities
                if storage.get("Amenity", a_id)
            ]
        )
        for p in all_places:
            p_amenities = None
            if getenv("HBNB_TYPE_STORAGE") == "db" and p.amenities:
                p_amenities = [a.id for a in p.amenities]
            elif len(p.amenities) > 0:
                p_amenities = p.amenities
            if p_amenities and all(
                [a in p_amenities for a in amenities]
            ):
                places_amenities.append(p)
    else:
        places_amenities = all_places
    result = [place.to_json() for place in places_amenities]
    return jsonify(result)
