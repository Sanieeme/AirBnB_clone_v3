#!/usr/bin/python4
"""
creates new view for place objects
"""
from models.city import City
from models.user import User
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models import storage


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places(city_id):
    """"retrieves the list"""
    city = storage.get(City, city_id)
    if not city:
        return abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """retrieves the place"""
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    return jsonify(place.to_dict())


@app_views.route('/cities/<city_id>/places', strict_slashes=False, methods=['POST'])
def post_place(city_id):
    """creates"""
    data = request.get_json()
    if not data:
       abort(400, "Not a JSON")
    if not storage.exists(City, city_id):
        return abort(404)
    if 'user_id' not in data:
        return abort(400, "Missing user_id")
    user_id = data['user_id']
    if not storage.exists(User, user_id):
        return abort(400, "Missing name")
    data['city_id'] = city_id
    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/place/<place_id>', strict_slashes=False, methods=['DELETE'])
def delete_place(place_id):
    """deletes"""
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200

@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def put_place(place_id):
    """updates"""
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    if request.content_type != 'application/json':
        return abort(400, "Not JSON")

    data = request.get_json()
    if not data:
        return abort(400, "Not a JSON")

    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()

    return jsonify(place.to_dict()), 200
