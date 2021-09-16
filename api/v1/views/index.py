#!/usr/bin/python3
""" index file """
from api.v1.views import app_views
from flask import request, jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def page_status():
    """ method which returns a json status ok """
    res = {"status": "OK"}
    return jsonify(res)
