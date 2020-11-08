from app import db
from flask_restful_swagger_3 import Schema
from app_models.cross_tables import user_order

class UserModel(Schema, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    user_type = db.Column(db.String(20))

    orders = db.relationship('OrderModel', secondary=user_order, lazy='subquery', backref=db.backref('user', lazy=True))


    def serialize(self):
        return {
            'id': self.id,
            'login': self.login,
            'email': self.email,
            'password': self.password,
            'user_type' : self.user_type,
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
        }