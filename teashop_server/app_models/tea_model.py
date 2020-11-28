from app import db
from flask_restful_swagger_3 import Schema

class TeaModel(db.Model):
    __tablename__ = 'tea'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    tea_type = db.Column(db.String(120)) 
    country = db.Column(db.String(120))
    stock = db.Column(db.Integer)
    descryption = db.Column(db.String(255))
    price = db.Column(db.Integer)

    photo_id = db.Column('photo_id', db.Integer, db.ForeignKey('photos.id'))

    photo = db.relationship('PhotoModel', lazy='select', backref=db.backref('tea', lazy='joined'))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'tea_type': self.tea_type,
            'country': self.country,
            'stock': self.stock,
            'descryption': self.descryption,
            'price': self.price
        }


class TeaSchema(Schema):
        type = 'object'
        properties = {
            'id':{
                'type': 'integer'
            },
            'name': {
                'type': 'string'
            },
            'teaType': {
                'type': 'string'
            },
            'country': {
                'type': 'string'
            },
            'stock':{
                'type': 'integer'
            },
            'descryption': {
                'type': 'string'
            },
            'price': {
                'type': 'integer'
            }
        }

class TeaPaginated(Schema):
        type = 'object'
        properties ={
            'page' : {
                'type': 'integer'
            },
            'pages': {
                'type': 'integer'
            },
            'perPage': {
                'type': 'integer'
            },
            'hasNext': {
                'type': 'boolean'
            },
            'hasPrev': {
                'type': 'boolean'
            },
            'total': {
                'type': 'integer'
            },
            'itemsNumber': {
                'type': 'integer'
            },
            'items': TeaSchema.array()
        }
