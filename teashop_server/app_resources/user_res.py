from flask import Response, abort, jsonify, request
from flask_restful_swagger_3 import Resource, swagger
from flask_restful import reqparse
from app_models.user_model import UserModel, UserSchema
from app import db


class UserRes(Resource):
    @swagger.tags(['User'])
    @swagger.reorder_with(UserSchema, description="Returns a user")    
    @swagger.parameter(_in='query', name='user_id', description='User ID',schema={'type': 'integer'},required=True)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, location='args')
        user_id = parser.parse_args().get('user_id')
        
        user = UserModel.query.filter_by(id=user_id).one_or_none()
        if user == None:
            return "toDoblald"

        response = jsonify(user.serialize())
        response.status_code = 200
        return response

    @swagger.tags(['User']) 
    @swagger.reorder_with(UserSchema, description="Post a user")
    @swagger.expected(UserSchema)
    def post(self):
        json = request.get_json()

        user = UserModel()
        user.email = json['email']
        user.login = json['login']
        user.password = json['password']
        user.user_type = json['user_type']

        try:
            db.session.add(user)
            db.session.commit()
        except Exception:
            return "toDoblald"


        response = jsonify(user.serialize())
        response.status_code = 200
        return response

    @swagger.tags(['User']) 
    @swagger.reorder_with(UserSchema, description="Put a user")
    @swagger.expected(UserSchema)
    @swagger.parameter(_in='query', name='user_id', description='User ID',schema={'type': 'integer'},required=True)
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, location='args')
        user_id = parser.parse_args().get('user_id')
        
        user = UserModel.query.filter_by(id=user_id).one_or_none()
        if user == None:
            return "toDoblald"

        json = request.get_json()

        user.email = json['email']
        user.login = json['login']
        user.password = json['password']
        user.user_type = json['user_type']

        try:
            db.session.add(user)
            db.session.commit()
        except Exception:
            return Exception

        response = jsonify(user.serialize())
        response.status_code = 200
        return response

