from flask import jsonify, g
from . import api

@api.route('news', methods = ['GET'])
def news():

	return jsonify({'status':'ok'})