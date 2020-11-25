from app import db
from flask_restful_swagger_3 import Schema
from app_models.cross_tables import user_order

class UserModel(Schema, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    user_type = db.relationship('UserTypeModel', lazy='select', backref=db.backref('user', lazy='joined'))


    orders = db.relationship('OrderModel', secondary=user_order, lazy='subquery', backref=db.backref('user', lazy=True))

    default_address = db.relationship('AddressModel', lazy='select', backref=db.backref('user', lazy='joined'))


    def serialize(self):
        return {
            'id': self.id,
            'login': self.login,
            'email': self.email,
            'password': self.password,
            'user_type' : self.user_type,
            'default_address' : self.default_address,
            'orders' : [order.id for order in self.orders]
        }

class UserSchema(Schema):
        type = 'object'
        properties = {
            'id':{
                'type': 'integer'
            },
            'login': {
                'type': 'string'
            },
            'email': {
                'type': 'string'
            },
            'password': {
                'type': 'string'
            },
            'user_type': {
                'type': 'string'
            },
            'default_address': {
                'type': 'integer'
            },
        }