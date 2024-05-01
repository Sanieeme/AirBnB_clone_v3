#!/usr/bin/python3
"""Views for the user objects"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User
from models.state import State


@app_views.route('/users', strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User)
    if users is None:
        abort(404)
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route('/users/<string:user_id>', strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Delete specific city objects"""
    user = storage.get(User, user_id)
    if user is not None:
        user.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/users',
                 strict_slashes=False,
                 methods=['POST'])
def post_user():
    """creates a new city object"""
    if not request.get_json() or request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    req = request.get_json()
    if 'email' not in req:
        abort(400, 'Missing email')
    if 'password' not in req:
        abort(400, 'Missing password')
    user = User(**req)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<string:user_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """updates a stored object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json() or request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    my_dict = request.get_json()
    not_include = ['id', 'email', 'state_id', 'created_at', 'updated_at']
    for key, val in my_dict:
        if key not in not_include:
            setattr(user, key, val)
    storage.save()
    return jsonify(user.to_dict()), 200
