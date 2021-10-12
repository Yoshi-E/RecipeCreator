from Webserver import app
from flask import jsonify, abort, make_response, url_for
from flask import Blueprint
from flask_restx import Api
from flask_httpauth import HTTPBasicAuth



auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'admin_test':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403) #uses 401 for login box

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

print("--------"*10)
print("Loading NLP Data")
from .editor import namespace as ns1, namespace2 as ns2



blueprint = Blueprint('api', __name__, url_prefix='/api') 
api_extension = Api(
    blueprint,
    title='Flask RESTx for NLP Recipe',
    version='1.0',
    description='Infterface to the core functions of the webtool <br><a href="/">Home</a>',
    doc='/doc'
)

api_extension.add_namespace(ns1)
api_extension.add_namespace(ns2)
app.register_blueprint(blueprint)


print("Loading Done!")
print("--------"*10)