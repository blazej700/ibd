from flask import Response, abort, jsonify, request
import flask
from flask_restful_swagger_3 import Resource, swagger, Schema
from flask_restful import reqparse
from app_models.order_model import OrderModel, OrderPaginated
from app_models.user_model import UserModel
from app_models.tea_model import TeaModel
from app_models.photo_model import PhotoModel
from commons.error import Error
from app import db
from sqlalchemy import or_, and_, desc
import os
import werkzeug

class PhotoSchema(Schema):
    media_type = 'image/png'
    type = 'string'
    format = 'binary'

class TeaPhotoRes(Resource):
    @swagger.tags(['Zdjęcia Herbat'])
    @swagger.response(description="Returns a photo of tea", response_code=200)   
    def get(self, tea_id):

        tea = TeaModel.query.filter_by(id=tea_id).one_or_none()
        if tea == None:
            return Error.getError(404, "Tea not found")
        return flask.send_file(os.path.abspath(tea.photo.path), as_attachment=False)

    @swagger.tags(['Zdjęcia Herbat'])
    @swagger.response(response_code = 200, description="Post a tea photo")
    @swagger.parameter(_in='query', name='files', description='Foto of tea NIE DZIAŁA NA SWAGGERZE, argument = file, lokalizacja files, in FormData',schema={'type': 'file'},required=True)
    @swagger.parameter(_in='header', name='Magic-key', description='Magic key',schema={'type': 'integer'},required=True)
    def put(self, tea_id):

        parser = reqparse.RequestParser()
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')

        parser.add_argument('Magic-key', type=int, location='headers')
        magic_key = parser.parse_args().get('Magic-key')
        if magic_key not in [1]:
            return Error.getError(401, "Unauthorized")

        args = parser.parse_args()
        file = args['file']

        tea = TeaModel.query.filter_by(id=tea_id).one_or_none()
        if tea == None:
            return Error.getError(404, "Tea not found")
        
        print(file)

        try:
            file.save(os.path.relpath('photo_store' + '/' + file.filename))
        except Exception:
            return Error.getError(500, "Internal server fuckup whuile saving photo on disk")

        teaPhoto = PhotoModel()
        teaPhoto.path = 'photo_store' + '/' + file.filename 

        try:
            db.session.add(teaPhoto)
            db.session.commit()
        except Exception as e:
            return Error.getError(500, "Internal server fuckup while saving photo in database")

        tea.photo_id = teaPhoto.id

        try:
            db.session.add(tea)
            db.session.commit()
        except Exception as e:
            return Error.getError(500, "Internal server fuckup whuile saving tea in database")

        response = jsonify(tea.serialize())
        response.status_code = 200
        return response