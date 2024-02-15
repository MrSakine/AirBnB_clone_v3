#!/usr/bin/python3
"""
This module is about python route
"""
from flask import Flask, render_template
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


@app.route("/python/")
@app.route("/python/<text>", strict_slashes=False)
def python(text: str = None):
    """Display text (Python + @text)"""
    if text is None:
        return "Python is cool"
    return f"Python {text.replace('_', ' ')}"


@app.route("/number/<int:n>", strict_slashes=False)
def n(n: int):
    """Display text (@n + is a number)"""
    return f"{n} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def n_template(n: int):
    """Display content from html files for the route"""
    return render_template('5-number.html', number=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def n_ood_or_even(n: int):
    """Display content from html files for the route"""
    return render_template('6-number_odd_or_even.html', number=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
