#!/usr/bin/python3
"""
Module to interface with the link between Places and Amenities
"""
from api.v1.views import (app_views, Place, Review, storage)
from flask import (request, jsonify, abort, make_response)


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def review_by_place(place_id=None):
    """
    Access the api call with on a place object to get its reviews
    returns a 404 if not found.
    - POST: Creates a new review object with the place_object linked
    - GET: Default, returns all review objects linked to the place.
    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if request.method == 'POST':
        posted_obj = request.get_json()
        if posted_obj is None:
            return("Not a JSON", 400)
        if 'user_id' not in posted_obj:
            return("Missing user_id", 400)
        user = storage.get(User, data['user_id'])
        if user is None:
            abort(404)
        if 'text' not in posted_obj:
            abort(400, description="Missing text")
        posted_obj['place_id'] = place_id
        new_obj = Review(**posted_obj)
        storage.save()
        return make_response(jsonify(new_obj.to_dict()), 201)
    else:
        review = []
        for rvw in place.reviews:
            review.append(rvw.to_dict())
        return (jsonify(review))


@app_views.route('reviews/<review_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def all_reviews(review_id=None):
    """
    Access the api call with on a place object to get its reviews
    returns a 404 if not found.
    - GET: Default, gets a review at <review_id>, status 200
    - DELETE: Deletes the review at id. Returns '{}', status 200
    - PUT:
    """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(storage.get('Review', review_id))
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        put_obj = request.get_json()
        if put_obj is None:
            abort(400, description="Not a JSON")
        instance = storage.get('Review', review_id)
        ignore_keys = ['id', 'user_id', 'place_id', 'updated_at', 'created_at']
        for attrib in put_obj:
            if attrib not in ignore_keys:
                setattr(instance, attrib, put_obj[attrib])
        instance.save()
        return make_response(jsonify(instance.to_dict()), 200)

    """ Default: GET """
    instance_get = storage.get('Review', review_id)
    return(jsonify(instance_get.to_dict()))
