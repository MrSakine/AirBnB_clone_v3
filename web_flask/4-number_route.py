#!/usr/bin/python3
"""
This module is about python route
"""

from flask import Flask
from werkzeug.routing import Rule

app = Flask(__name__)


@app.endpoint("default_python")
def default_python():
    return "Python is cool"


@app.route("/", strict_slashes=False)
def hello_hbnb():
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c(text: str):
    return f"C {text.replace('_', ' ')}"


@app.route("/python/<text>", strict_slashes=False)
def python(text: str = "cool"):
    return f"Python {text.replace('_', ' ')}"


@app.route("/number/<int:n>", strict_slashes=False)
def n(n: int):
    return f"{n} is a number"


app.url_map.add(Rule("/python/", endpoint="default_python"))


app.run()
