from flask import Flask
from flask_restful import Api, Resource, reqparse

from controllers import api

app = Flask(__name__)

app.register_blueprint(api)

app.run(debug=True)