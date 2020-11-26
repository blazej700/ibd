from flask import Response, abort, jsonify, request
from flask_restful_swagger_3 import Resource, swagger
from flask_restful import reqparse
from app_models.order_model import OrderModel, OrderPaginated
from app_models.order_status_model import OrderStatusModel
from app_models.user_type_model import UserTypeModel
from app import db
from commons.error import Error

class DevTools(Resource):
    @swagger.tags(['DevTools'])
    @swagger.response(response_code=200, description="Orders statuses and users types")   
    def get(self):
        
        order_statuss = OrderStatusModel.query.all()

        order_status_list = []
        [order_status_list.append(order_status.serialize()) for order_status in order_statuss]
        
        user_types = UserTypeModel.query.all()

        user_types_list = []
        [user_types_list.append(user_type.serialize()) for user_type in user_types]


        response = jsonify({'ordersStatuses': order_status_list, 'userTypes' : user_types_list})
        response.status_code = 200
        return response