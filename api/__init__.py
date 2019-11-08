from flask import request, g, jsonify,Blueprint
api = Blueprint('api', __name__)
from . import news, errors
