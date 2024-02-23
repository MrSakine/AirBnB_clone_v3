#!/usr/bin/python3
"""
This module is about the blueprint of the API
"""
from flask import Blueprint, render_template, abort

app_views = Blueprint("app_views", __name__)
