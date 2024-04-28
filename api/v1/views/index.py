#!/usr/bin/python3
"""
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity


@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})


@app.route('/api/v1/stats')
def stats():
    stat = {}
    classes = {
               "amenities": Amenity,
               "cities": City,
               "places": Place,
               "reviews": Review,
               "states": State,
               "users": User
             }

    for clss, cls in classes.items():
        count = storage.count(cls)
        stat[clss] = count
    return jsonify(stat)
