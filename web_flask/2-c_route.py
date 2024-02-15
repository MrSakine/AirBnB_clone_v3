#!/usr/bin/python3
"""
This module is a minimal flask code & 2 route
"""

from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c(text: str):
    return f"C {text.replace('_', ' ')}"


app.run()
