#!/usr/bin/python3
"""
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def stats():
    stat = {}
    classes = {'amenities': Amenity,
               'cities': City,
               'places': Place,
               'reviews': Review,
               'states': State,
               'users': User
             }

    for clss, cls in classes.items():
        count = storage.count(cls)
        stat[clss] = count
    return jsonify(stat)
