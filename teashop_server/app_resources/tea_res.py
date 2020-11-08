from flask import Response, abort, jsonify, request
from flask_restful_swagger_3 import Resource, swagger
from flask_restful import reqparse
from app_models.tea_model import TeaModel, TeaSchema
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
            return "toDoblald"

        response = jsonify(user.serialize())
        response.status_code = 200
        return response


    @swagger.tags(['Herbatka'])
    @swagger.reorder_with(TeaSchema, description="Post a tea")
    @swagger.expected(TeaSchema)   
    def post(self):
        json = request.get_json()

        tea = TeaModel()
        tea.country = json['country']
        tea.descryption = json['descryption']
        tea.name = json['name']
        tea.stock = json['stock']
        tea.price = json['price']
        tea.tea_type = json['teaType']


        try:
            db.session.add(tea)
            db.session.commit()
        except Exception:
            return "toDoblald"


        response = jsonify(tea.serialize())
        response.status_code = 200
        return response