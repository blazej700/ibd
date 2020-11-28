from flask import Response, abort, jsonify, request
from flask_restful_swagger_3 import Resource, swagger, Schema
from flask_restful import reqparse
from commons.error import Error
from app_models.login_model import LoginSchema
from app_models.magic_key_model import KeySchema
from app_models.user_model import UserModel
from app_models.user_type_model import UserTypeModel
from sqlalchemy import or_

class LoginRes(Resource):

    @swagger.tags(['Logowanie'])
    @swagger.reorder_with(KeySchema, description="Login")
    @swagger.expected(LoginSchema) 
    def post(self):
        json = request.get_json()

        user = UserModel()
        if 'loginOrEmail' in json:
            user = UserModel.query.filter(or_(UserModel.login == json['loginOrEmail'],  UserModel.email == json['loginOrEmail'])).one_or_none()
            if user == None:
                return Error.getError(401, "WrOnG LoGiN oR eMaIl!")
        else:
            return Error.getError(400, "How can I find user, when you not give login or name??????????")

        if 'password' in json:
            if json['password'] != user.password:
                return Error.getError(401, "Bad password, silly tiny hacker!")
        else:
            return Error.getError(400, "Ok, I have a user, but now I need a password! I should made a limit for dump requests!!!")

        response = jsonify({'key' : user.id, 'userType': user.user_type.user_type_name})
        response.status_code = 200
        return response
