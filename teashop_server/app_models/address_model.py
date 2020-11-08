from app import db
from flask_restful_swagger_3 import Schema

class AddressModel(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(120))
    city = db.Column(db.String(120))
    street = db.Column(db.String(120))
    number = db.Column(db.String(120))
    postal_code = db.Column(db.String(120))

    def serialize(self):
        return {
            'id': self.id,
            'country': self.country,
            'city': self.city,
            'street': self.street,
            'number': self.number,
            'postal_code': self.postal_code
        }

class AddressSchema(Schema):
    type = 'object'
    properties = {
        'id':{
            'type': 'integer'
        },
        'country': {
            'type': 'string'
        },
        'city': {
            'type': 'string'
        },
        'street': {
            'type': 'string'
        },
        'number': {
            'type': 'string'
        },
        'postal_code': {
            'type': 'string'
        }
    }