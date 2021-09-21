#!/usr/bin/python3
"""
Module to interface with the link between Places and Amenities
"""
from api.v1.views import (app_views, Place, Amenity, storage)
from flask import (request, jsonify, abort, make_response)
from os import environ


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'],
                 strict_slashes=False)
def amenity_by_place(place_id=None):
    """
    Access the api call with on a place object to get its amenities
    returns a 404 if not found.
    - POST: Creates a new amenity object with the linked place object
    - DELETE: Default, returns all amenity objects linked to the place.
    """
    amenities = []
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == 'db':
        for amn in place.amenities:
            amenities.append(amn.to_dict())
    else:
        for amn_id in place.amenity_ids:
            amenities.append(storage.get(Amenity, amn_id).to_dict())
    return(jsonify(amenities))


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'],
                 strict_slashes=False)
def manipulate_amenties_place(place_id, amenity_id):
    """
    Access the api call with on a place object to get its amenities
    returns a 404 if not found.
    - DELETE:
    Deletes the link between Amenity objects and Place objects
    If the Amenity is not linked to the Place before the request,
    raise a 404 error
    Returns an empty dictionary with the status code 200
    - POST:
    Link a Amenity object to a Place
    If the Amenity is already linked to the Place,
    return the Amenity with the status code 200
    Returns the Amenity with the status code 201
    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if request.method == 'DELETE':
        if environ.get('HBNB_TYPE_STORAGE') == 'db':
            if amenity not in place.amenities:
                abort(404)
            place.amenities.remove(amenity)
        else:
            if amenity_id not in place.amenity_ids:
                abort(404)
            place.amenity_ids.remove(amenity_id)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'POST':
        if environ.get('HBNB_TYPE_STORAGE') == 'db':
            if amenity in place.amenities:
                return make_response(jsonfiy(amenity.to_dict()), 200)
            else:
                place.amenities.append(amenity)
        else:
            if amenity_id in place.amenity_ids:
                return make_response(jsonfiy(amenity.to_dict()), 200)
            else:
                place.amenity_ids.append(amenity_id)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 201)
