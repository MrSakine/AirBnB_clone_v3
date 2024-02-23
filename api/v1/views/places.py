#!/usr/bin/python3
"""Place objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place


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
def post_places_search():
    """searches for a place"""
    if request.get_json() is not None:
        params = request.get_json()
        states = params.get("states", [])
        cities = params.get("cities", [])
        amenities = params.get("amenities", [])
        amenity_objects = []
        for amenity_id in amenities:
            amenity = storage.get("Amenity", amenity_id)
            if amenity:
                amenity_objects.append(amenity)
        if states == cities == []:
            places = storage.all("Place").values()
        else:
            places = []
            for state_id in states:
                state = storage.get("State", state_id)
                state_cities = state.cities
                for city in state_cities:
                    if city.id not in cities:
                        cities.append(city.id)
            for city_id in cities:
                city = storage.get("City", city_id)
                for place in city.places:
                    places.append(place)
        confirmed_places = []
        for place in places:
            place_amenities = place.amenities
            confirmed_places.append(place.to_dict())
            for amenity in amenity_objects:
                if amenity not in place_amenities:
                    confirmed_places.pop()
                    break
        return jsonify(confirmed_places)
    else:
        abort(400, "Not a JSON")
