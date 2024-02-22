#!/usr/bin/python3
"""
This module is about the route of the API
"""
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """Return the status of the server"""
    return {"status": "OK"}
