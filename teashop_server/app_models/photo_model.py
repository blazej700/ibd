from app import db
from flask_restful_swagger_3 import Schema

class PhotoModel(db.Model):
    __tablename__ = 'photos'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(10))
    photo_type = db.Column(db.String(120))