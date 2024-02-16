#!/usr/bin/python3
"""
This module is about listing states from db
"""
from models import storage
from models.state import State
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/states", strict_slashes=False)
@app.route("/states/<id>", strict_slashes=False)
def states(id=None):
    """Display content from html files for the route"""
    all_states = storage.all(cls=State)
    state = None
    if id is not None:
        for s in all_states.values():
            if s.id == id:
                state = s
                break
    return render_template(
        "9-states.html",
        states=all_states,
        state=state,
        id=id
    )


@app.teardown_appcontext
def close_storage(exception):
    """Close sqlalchemy session after each request"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
