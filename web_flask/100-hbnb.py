#!/usr/bin/python3
"""
This module is about listing states, city,
amenities & places from db
"""
from models import storage
from flask import Flask, render_template
from models.state import State
from models.amenity import Amenity
from models.place import Place

app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """Display content from html files for the route"""
    all_states = storage.all(cls=State)
    all_amenities = storage.all(cls=Amenity)
    all_places = storage.all(cls=Place)

    return render_template(
        "10-hbnb_filters.html",
        states=all_states,
        amenities=all_amenities,
        places=all_places
    )


@app.teardown_appcontext
def close_storage(exception):
    """Close sqlalchemy session after each request"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
