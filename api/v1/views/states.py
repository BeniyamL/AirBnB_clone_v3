#!/usr/bin/python3
""" a view to hanlde default REST api actions for state object"""
from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """ method which gets all state objects"""
    all_states = storage.all(State).values()
    all_state_dct = []
    for state in all_states:
        all_state_dct.append(state.to_dict())
    return jsonify(all_state_dct)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def single_state(state_id):
    """ method to get a single state object """
    state = storage.get(State, state_id)
    if state is None:
        abort(404, 'Not found')
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ a method to delete a state based on state id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404, 'Not found')
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ a method to create a new state """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if data.get("name") is None:
        abort(400, 'Missing name')
    obj = State(**data)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ a method to update an existing state """
    state = storage.get(State, state_id)
    if state is None:
        abort(404, 'Not found')
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'created_at', 'updated_at']

    for k, v in data.items():
        if k not in ignore_keys:
            setattr(state, k, v)

    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
