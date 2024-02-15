#!/usr/bin/python3
"""
This module is about listing states from db
"""
from models import storage
from models.state import State
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def states_list():
    """Display content from html files for the route"""
    all_states = storage.all(cls=State)
    return render_template("7-states_list", states=all_states)


@app.teardown_appcontext
def close_storage(exception):
    """Close sqlalchemy session after each request"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
