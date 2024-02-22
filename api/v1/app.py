#!/usr/bin/python3
"""
This module is the root of the API
"""
import os
from models import storage
from api.v1.views.index import app_views
from flask import Flask

app = Flask(__name__)

app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def close_storage(exception):
    """Close sqlalchemy session after each request"""
    storage.close()


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST") if os.getenv(
        "HBNB_API_HOST") is not None else "0.0.0.0"
    port = int(os.getenv("HBNB_API_PORT")) if os.getenv(
        "HBNB_API_PORT") is not None else 5000
    app.run(host=host, port=port, threaded=True)
