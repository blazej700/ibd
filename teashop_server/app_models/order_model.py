from app import db
from flask_restful_swagger_3 import Schema
from app_models.tea_model import TeaSchema
from app_models.address_model import AddressSchema
from app_models.cross_tables import order_tea, user_order

class OrderModel(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    details = db.Column(db.String(255))


    #status = db.Column(db.String(255))

    status_id = db.Column('status_id', db.Integer, db.ForeignKey('order_status.id'))
    status = db.relationship('OrderStatusModel', lazy='select', backref=db.backref('order', lazy='joined')) 


    address_id = db.Column('address_id', db.Integer, db.ForeignKey('address.id'))
    address = db.relationship('AddressModel', lazy='select', backref=db.backref('order', lazy='joined'))

    teas = db.relationship('TeaModel', secondary=order_tea, lazy='subquery', backref=db.backref('order', lazy=True))

    ordered_by = db.relationship('UserModel', secondary=user_order, lazy='subquery', backref=db.backref('order', lazy=True))

    def serialize(self):
        return {
            'id': self.id,
            'details': self.details,
            'status': self.status.name,
            'address': self.address.serialize(),
            'teas': [tea.serialize() for tea in self.teas],
            'orderedBy': self.ordered_by[0].id if self.ordered_by[0] is not None else None
        }

class IntegerSchema(Schema):
    type = 'integer'


class OrderCreateSchema(Schema):
    type = 'object'
    properties = {
        'id':{
            'type': 'integer'
        },
        'status': {
            'type': 'integer'
        },
        'details': {
            'type': 'string'
        },
        'orderedBy':{
            'type': 'integer'
        },
        'address': AddressSchema,
        'teaIds':IntegerSchema.array()
    }

class OrderStatusSchema(Schema):
    type = 'object'
    properties = {
        'status': {
            'type': 'integer'
        }
        }

class OrderSchema(Schema):
    type = 'object'
    properties = {
        'id':{
            'type': 'integer'
        },
        'status': {
            'type': 'string'
        },
        'details': {
            'type': 'string'
        },
        'orderedBy':{
            'type': 'integer'
        },
        'addresses': AddressSchema,
        'teas': TeaSchema.array()
        
    }

class OrderPaginated(Schema):
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
            'items': OrderSchema.array()
        }