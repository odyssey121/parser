from flask import Blueprint
api = Blueprint('api', __name__) 
from flask import request, g
from . import news



def not_found(message):
	response = jsonify({'status':'forbidden', 'message': message})
	response.status_code = 404
	return response


@api.errorhandler(404)
def not_found_handler(e):
	return not_found('resource not found')