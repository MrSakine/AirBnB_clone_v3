#!/usr/bin/python3
"""
This module is a minimal flask code
"""

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello HBNB!"


app.run()
