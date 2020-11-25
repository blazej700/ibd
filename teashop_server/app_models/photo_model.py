from app import db
from flask_restful_swagger_3 import Schema

class PhotoModel(Schema, db.Model):
    __tablename__ = 'order_status'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(10))