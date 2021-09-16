#!/usr/bin/python3
""" index file """
from api.v1.views import app_views
from flask import request, jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def page_status():
    """ method which returns a json status ok """
    res = {"status": "OK"}
    return jsonify(res)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def obj_count():
    """ retrieve the number of each objects by type """
    classes = [Amenity, City, Place, Review, State, User]
    literals = ["amenities", "cities", "places", "reviews", "states", "users"]

    count_dict = {}
    for j in range(len(classes)):
        count_dict[literals[j]] = storage.count(classes[j])

    return jsonify(count_dict)
