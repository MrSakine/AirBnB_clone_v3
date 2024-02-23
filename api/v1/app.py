#!/usr/bin/python3
"""
This module is the root of the API
"""
import os
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, make_response

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, resources={"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def close_storage(exception):
    """Close sqlalchemy session after each request"""
    storage.close()


@app.errorhandler(400)
def handle_400_error(e):
    """Handle 400 error"""
    message = jsonify({"error": e.description})
    return make_response(message, 400)


@app.errorhandler(404)
def handle_404_error(e):
    """Handle 404 error"""
    message = jsonify({"error": "Not found"})
    return make_response(message, 404)


if __name__ == "__main__":
    host = (
        os.getenv("HBNB_API_HOST")
        if os.getenv("HBNB_API_HOST") is not None
        else "0.0.0.0"
    )
    port = (
        int(os.getenv("HBNB_API_PORT"))
        if os.getenv("HBNB_API_PORT") is not None
        else 5000
    )
    app.run(host=host, port=port, threaded=True)
