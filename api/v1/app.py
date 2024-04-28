#!/usr/bin/python3
"""
return the status of your API
"""


from flask import Flask
from flask import Blueprint
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()


if __name__ == "__main__":
    import os

    h = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    p = int(os.environ.get('HBNB_API_PORT', 5001))

    app.run(host=h, port=p, threaded=True)
