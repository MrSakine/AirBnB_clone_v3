#!/usr/bin/python3
"""
This module is a minimal flask code
"""

from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    return "Hello HBNB!"


app.run()
