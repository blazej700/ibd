from flask import Response, abort, jsonify, request
from flask_restful_swagger_3 import Resource, swagger
from flask_restful import reqparse
from app_models.tea_model import TeaModel, TeaSchema
from app_models.photo_model import PhotoModel
from app_models.ordered_teas import OrderedTeas
from commons.error import Error
from app import db

class TeaRes(Resource):
    @swagger.tags(['Herbatka'])
    @swagger.reorder_with(TeaSchema, description="Returns a tea")    
    @swagger.parameter(_in='query', name='tea_id', description='Tea ID',schema={'type': 'integer'},required=True)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('tea_id', type=int, location='args')
        tea_id = parser.parse_args().get('tea_id')
        
        user = TeaModel.query.filter_by(id=tea_id).one_or_none()
        if user == None:
            return Error.getError(404, "Tea not found")

        response = jsonify(user.serialize())
        response.status_code = 200
        return response


    @swagger.tags(['Herbatka'])
    @swagger.reorder_with(TeaSchema, description="Post a tea")
    @swagger.expected(TeaSchema)   
    @swagger.parameter(_in='header', name='Magic-key', description='Magic key',schema={'type': 'integer'},required=True)
    def post(self):
        json = request.get_json()

        parser = reqparse.RequestParser()
        parser.add_argument('Magic-key', type=int, location='headers')
        magic_key = parser.parse_args().get('Magic-key')
        print(magic_key)
        if magic_key not in [1]:
            return Error.getError(401, "Unauthorized")


        tea = TeaModel()
        tea.country = json['country']
        tea.descryption = json['descryption']
        tea.name = json['name']
        tea.stock = json['stock']
        tea.price = json['price']
        tea.tea_type = json['teaType']
        tea.photo_id = 1

        try:
            db.session.add(tea)
            db.session.commit()
        except Exception as e:
            #print(e)
            return Error.getError(500, "Internal server eroror in database while adding tea")


        response = jsonify(tea.serialize())
        response.status_code = 200
        return response

    @swagger.tags(['Herbatka'])
    @swagger.reorder_with(TeaSchema, description="Update a tea")
    @swagger.expected(TeaSchema)   
    @swagger.parameter(_in='header', name='Magic-key', description='Magic key',schema={'type': 'integer'},required=True)
    @swagger.parameter(_in='query', name='tea_id', description='Tea ID',schema={'type': 'integer'},required=True)
    def put(self):
        json = request.get_json()

        parser = reqparse.RequestParser()
        parser.add_argument('Magic-key', type=int, location='headers')
        parser.add_argument('tea_id', type=int, location='args')
        
        tea_id = parser.parse_args().get('tea_id')
        magic_key = parser.parse_args().get('Magic-key')

        if magic_key not in [1]:
            return Error.getError(401, "Unauthorized")

        tea = TeaModel.query.filter_by(id=tea_id).one_or_none()
        if tea == None:
            return Error.getError(404, "Tea not found")


        tea.country = json['country']
        tea.descryption = json['descryption']
        tea.name = json['name']
        tea.stock = json['stock']
        tea.price = json['price']
        tea.tea_type = json['teaType']

        try:
            db.session.add(tea)
            db.session.commit()
        except Exception as e:
            return Error.getError(500, "Internal server eroror in database while adding tea")


        response = jsonify(tea.serialize())
        response.status_code = 200
        return response


    @swagger.tags(['Herbatka'])
    @swagger.reorder_with(TeaSchema, description="Delete a tea")    
    @swagger.parameter(_in='query', name='tea_id', description='Tea ID',schema={'type': 'integer'},required=True)
    @swagger.parameter(_in='header', name='Magic-key', description='Magic key',schema={'type': 'integer'},required=True)
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Magic-key', type=int, location='headers')
        parser.add_argument('tea_id', type=int, location='args')
        
        tea_id = parser.parse_args().get('tea_id')
        magic_key = parser.parse_args().get('Magic-key')

        if magic_key not in [1]:
            return Error.getError(401, "Unauthorized")

        tea = TeaModel.query.filter_by(id=tea_id).one_or_none()
        if tea == None:
            return Error.getError(404, "Tea not found")

        try:
            db.session.delete(tea)
            db.session.commit()
        except Exception as e:
            return Error.getError(500, "Internal server eroror in database while adding tea")

        response = Response()
        response.status_code = 200
        return response


        