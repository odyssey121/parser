from flask import jsonify, g
from . import api
from app.module import parser

@api.route('news', methods = ['GET'])
def news():
	news = parser.main()
	print(news)
	return jsonify(news)