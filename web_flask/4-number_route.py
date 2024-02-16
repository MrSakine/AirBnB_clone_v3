#!/usr/bin/python3
"""
This module is about python route
"""
from flask import Flask

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
    return "C {}".format(text.replace('_', ' '))


@app.route("/python/", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python(text: str = None):
    """Display text (Python + @text)"""
    if text is None:
        return "Python is cool"
    return "Python {}".format(text.replace('_', ' '))


@app.route("/number/<int:n>", strict_slashes=False)
def n(n):
    """Display text (@n + is a number)"""
    return "{} is a number".format(n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
