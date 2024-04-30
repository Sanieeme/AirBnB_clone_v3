#!/usr/bin/python3
"""
"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/states', strict_slashes=False)
def all():
    states = storage.all(State)
    return jsonify([state.to_dict() for state in states.values()])


@app_views.route('/states/<state_id>', strict_slashes=False)
def get(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(
        '/states/<state_id>',
        strict_slashes=False,
        methods=['DELETE']
        )
def delete(state_id):
    state = storage.get(State, state_id)
    if state:
        state.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def post():
    req = request.get_json()
    if not req:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in req:
        return jsonsonify({"error": "Missing name"}), 400
    state = State(**req)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def put(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, 'Not a JSON')
    state.name = req['name']
    storage.save()
    return jsonify(state.to_dict()), 200
