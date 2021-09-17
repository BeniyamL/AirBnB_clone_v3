#!/usr/bin/python3
""" a view to hanlde default REST api actions for city object"""
from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    """ method which gets all cities objects"""
    state = storage.get(State, str(state_id))
    if state is None:
        abort(404, 'Not found')
    all_cities = storage.all(City).values()
    all_city_dct = []
    for city in all_cities:
        if city.state_id == str(state_id):
            all_city_dct.append(city.to_dict())
    return jsonify(all_city_dct)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def single_city(city_id):
    """ method to get a single city object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404, 'Not found')
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ a method to delete a city based on city id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404, 'Not found')
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ a method to create a new city """
    state = storage.get(State, state_id)
    if state is None:
        abort(404, 'Not found')
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if data.get("name") is None:
        abort(400, 'Missing name')
    data['state_id'] = str(state_id)
    obj = City(**data)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ a method to update an existing city """
    city = storage.get(City, city_id)
    if city is None:
        abort(404, 'Not found')
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']

    for k, v in data.items():
        if k not in ignore_keys:
            setattr(city, k, v)

    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
