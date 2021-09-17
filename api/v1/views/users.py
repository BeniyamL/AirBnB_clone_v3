#!/usr/bin/python3
""" a view to hanlde default REST api actions for user object"""
from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """ method which gets all user objects"""
    all_users = storage.all(User).values()
    all_user_dct = []
    for user in all_users:
        all_user_dct.append(user.to_dict())
    return jsonify(all_user_dct)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def single_user(user_id):
    """ method to get a single user object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404, 'Not found')
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ a method to delete a user based on user id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404, 'Not found')
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ a method to create a new user """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if data.get("email") is None:
        abort(400, 'Missing email')
    if data.get("password") is None:
        abort(400, 'Missing password')
    obj = User(**data)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ a method to update an existing user """
    user = storage.get(User, user_id)
    if user is None:
        abort(404, 'Not found')
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']

    for k, v in data.items():
        if k not in ignore_keys:
            setattr(user, k, v)

    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
