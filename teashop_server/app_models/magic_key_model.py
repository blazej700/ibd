from flask_restful_swagger_3 import Schema

class KeySchema(Schema):
    type = 'object'
    properties = {
        'key': {
            'type': 'integer'
        }
    }