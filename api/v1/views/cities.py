#!/usr/bin/python3
"""Views for the city objects"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities', strict_slashes=False)
def get_cities(state_id):
    """get city information for all cities in a specified state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<string:city_id>', strict_slashes=False)
def get_city(city_id):
    """get city information for specified city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Delete specific city objects"""
    city = storage.get(City, city_id)
    if city is not None:
        city.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/<string:state_id>/cities',
                 strict_slashes=False,
                 methods=['POST'])
def post_city(state_id):
    """creates a new city object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json() or request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    req = request.get_json()
    if 'name' not in req:
        abort(400, 'Missing name')
    req['state_id'] = state_id
    city = City(**req)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<string:city_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """updates a stored object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    my_dict = request.get_json()
    not_include = ['id', 'state_id', 'created_at', 'updated_at']
    for key, val in my_dict:
        if key not in not_include:
            setattr(city, key, val)
    storage.save()
    return jsonify(city.to_dict()), 200
