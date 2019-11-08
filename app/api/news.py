
from flask import jsonify, g, request
from app.modules.parser import Parser
from . import api
from . errors import bad_request, not_found


@api.route('news', methods=['POST'])
def getNews():
    content = request.json
    if type(content) == dict:
        parser = Parser(content)
        response = parser.start()
        return jsonify(response)
    return bad_request('requested data types do not match')
