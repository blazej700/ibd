from app import db
from flask_restful_swagger_3 import Schema

class UserTypeModel(Schema, db.Model):
    __tablename__ = 'user_type'
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(20))

    def serialize(self):
        return {
            'id': self.id,
            'user_type' : self.user_type,
        }