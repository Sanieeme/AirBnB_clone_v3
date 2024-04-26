#!/usr/bin/python3
"""
"""
from api.v1.views import app_views
from flask import Flask, jsonify


app = Flask(__name__)

@app.route('/status')
def status():
    return jsonify({"status": "OK"})


if __name__ == "__main__":
    app.run(debug=True)
