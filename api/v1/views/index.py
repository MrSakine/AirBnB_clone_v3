#!/usr/bin/python3
"""
This module is about the route of the API
"""
from models import storage
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """Return the status of the server"""
    return {"status": "OK"}


@app_views.route("/stats")
def stats():
    """Show stats about the stored objects"""
    class_list = [Amenity, City, State, Place, Review, User]
    names = ["amenities", "cities", "states", "places", "reviews", "users"]
    res = {}
    for name, cls in zip(names, class_list):
        res[name] = storage.count(cls=cls)
    return res
