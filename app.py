from flask import Flask

from controllers import api

app = Flask(__name__)

app.register_blueprint(api)

app.run(debug=True)
