from flask_restful_swagger_3 import Schema

class LoginSchema(Schema):
    type = 'object'
    properties = {
        'loginOrEmail': {
        'type': 'string'
        },
        'password': {
            'type': 'string'
        }
    }