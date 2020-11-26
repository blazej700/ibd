import json
from datetime import datetime
from flask import jsonify

class Error:

    @staticmethod
    def getError(code, msg):
        response = jsonify({"info": "BABOL", "message" : msg,  "timestamp":  str(datetime.utcnow()), "BABOL" : "BABOL"})
        response.status_code = code
        return response



