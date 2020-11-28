from app import db
from flask_restful_swagger_3 import Schema

class UserTypeModel(db.Model):
    __tablename__ = 'user_type'
    id = db.Column(db.Integer, primary_key=True)
    user_type_name = db.Column(db.String(20))

    def serialize(self):
        return {
            'id': self.id,
            'user_type_name' : self.user_type_name,
        }
