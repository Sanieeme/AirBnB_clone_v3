#!/usr/bin/python3
"""
"""
from api.v1.views import app_views
from flask import jsonify


<<<<<<< HEAD
@app.route('/status')
def status():
    return jsonify({"status": "OK"}):wq
=======
@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})
>>>>>>> b42a31b84845eb858707cc9fbfcff042344102e6
