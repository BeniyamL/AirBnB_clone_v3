#!/usr/bin/python3
""" a view to hanlde default REST api actions for amenity object"""
from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """ method which gets all amenity objects"""
    all_amenities = storage.all(Amenity).values()
    all_amenity_dct = []
    for amenity in all_amenities:
        all_amenity_dct.append(amenity.to_dict())
    return jsonify(all_amenity_dct)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def single_amenity(amenity_id):
    """ method to get a single amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404, 'Not found')
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ a method to delete an amenity based on amenity id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404, 'Not found')
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ a method to create a new amenity """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if data.get("name") is None:
        abort(400, 'Missing name')
    obj = Amenity(**data)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ a method to update an existing amenity """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404, 'Not found')
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'created_at', 'updated_at']

    for k, v in data.items():
        if k not in ignore_keys:
            setattr(amenity, k, v)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
