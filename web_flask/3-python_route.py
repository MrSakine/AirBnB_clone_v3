#!/usr/bin/python3
"""
This module is about python route
"""
from flask import Flask
from werkzeug.routing import Rule

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """Base route"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """hbnb route"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c(text: str):
    """Display text (C + @text)"""
    return f"C {text.replace('_', ' ')}"


@app.route("/python/", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python(text: str = None):
    """Display text (Python + @text)"""
    if text is None:
        return "Python is cool"
    return f"Python {text.replace('_', ' ')}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
