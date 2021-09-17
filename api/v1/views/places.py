#!/usr/bin/python3
""" a view to hanlde default REST api actions for place object"""
from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from models.city import City
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places(city_id):
    """ method which gets all place objects"""
    city = storage.get(City, str(city_id))
    if city is None:
        abort(404, 'Not found')
    all_places = storage.all(Place).values()
    all_place_dct = []
    for place in all_places:
        if place.city_id == str(city_id):
            all_place_dct.append(place.to_dict())
    return jsonify(all_place_dct)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def single_place(place_id):
    """ method to get a single place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, 'Not found')
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ a method to delete a place based on place id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, 'Not found')
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ a method to create a new place """
    city = storage.get(City, city_id)
    if city is None:
        abort(404, 'Not found')
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if data.get("user_id") is None:
        abort(400, 'Missing user_id')
    if data.get("name") is None:
        abort(400, "Missing name")
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404, 'Not found')
    data['city_id'] = str(city_id)
    obj = Place(**data)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ a method to update an existing place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, 'Not found')
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'user_id','city_id', 'created_at', 'updated_at']

    for k, v in data.items():
        if k not in ignore_keys:
            setattr(place, k, v)

    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
