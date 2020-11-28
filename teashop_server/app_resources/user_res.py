from flask import Response, abort, jsonify, request
from flask_restful_swagger_3 import Resource, swagger
from flask_restful import reqparse
from app_models.user_model import UserModel, UserSchema
from app_models.address_model import AddressModel
from app_models.user_type_model import UserTypeModel
from commons.error import Error
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
            return Error.getError(404, "User not found")

        response = jsonify(user.serialize())
        response.status_code = 200
        return response

    @swagger.tags(['User']) 
    @swagger.reorder_with(UserSchema, description="Post a user, userType 1-admin, 2")
    @swagger.expected(UserSchema)
    def post(self):
        json = request.get_json()

        user = UserModel()
        user.email = json['email']
        user.login = json['login']
        user.password = json['password']
        user.user_type = json['user_type']

        address = AddressModel()
        json_address = json['address']
        if 'id' in json_address:
            address = AddressModel.query.filter_by(id=json_address['id']).one_or_none()
            if address == None:
                return Error.getError(404, "Address not found")
        else:
            address.number = json_address['number']
            address.city = json_address['city']
            address.country = json_address['country']
            address.street = json_address['street']
            address.postal_code = json_address['postal_code']
            try:
                db.session.add(address)
            except Exception:
                return Error.getError(500, "Internal server eroror in database while adding user")

        user.address = address

        try:
            db.session.add(user)
            db.session.commit()
        except Exception:
            return Error.getError(500, "Internal server eroror in database while adding user")


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
            return Error.getError(404, "Users not found")

        json = request.get_json()

        user.email = json['email']
        user.login = json['login']
        user.password = json['password']
        user.user_type = json['user_type']

    
        try:
            db.session.add(user)
            db.session.commit()
        except Exception:
            return Error.getError(500, "Internal server eroror in database while vladimir PUTin user")

        response = jsonify(user.serialize())
        response.status_code = 200
        return response

