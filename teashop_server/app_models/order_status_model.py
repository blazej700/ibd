from app import db
from flask_restful_swagger_3 import Schema

class OrderStatusModel(db.Model):
    __tablename__ = 'order_status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }
