from app import db
from flask_restful_swagger_3 import Schema

class OrderedTeas(db.Model):
    __tablename__ = 'ordered_teas'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column('order_id', db.Integer, db.ForeignKey('order.id'))
    
    tea_id = db.Column('tea_id', db.Integer, db.ForeignKey('tea.id'))
    
    #tea = db.relationship('Tea', lazy='select', backref=db.backref('ordered_teas', lazy='joined'))
    
    quantity = db.Column('quantity', db.Integer)

    def serialize(self):
        return {
            'id': self.id,
            'quantity': self.quantity,
            'teaId': self.tea_id,
        }

class OrderedTeasSchema(Schema):
    type = 'object'
    properties = {
        'id':{
            'type': 'integer'
        },
        'teaId': {
            'type': 'integer'
        },
        'quantity': {
            'type': 'integer'
        }
    }