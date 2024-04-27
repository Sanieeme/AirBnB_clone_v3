#!/usr/bin/python3
"""
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


storage = storage()


@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})


@app.route('/api/v1/stats', methods='GET')
def stats():
    stat = {}
    for clss, cls in storage.classes.items():
        count = storage.count(cls)
        stats[clss] = count
    return jsonify(stat)
