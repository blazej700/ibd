from app_models.tea_model import TeaModel
from flask import Response, abort, jsonify, request
from flask_restful_swagger_3 import Resource, swagger
from flask_restful import reqparse
from app_models.order_model import OrderModel, OrderSchema, OrderCreateSchema, OrderStatusSchema
from app_models.address_model import AddressModel
from app_models.user_model import UserModel
from app_models.order_status_model import OrderStatusModel
from app import db
from commons.error import Error

class OrderRes(Resource):
    @swagger.tags(['Zamówienia'])
    @swagger.reorder_with(OrderSchema, description="Returns a order")    
    @swagger.parameter(_in='query', name='order_id', description='Order ID',schema={'type': 'integer'},required=True)
    @swagger.parameter(_in='header', name='Magic-key', description='Magic key',schema={'type': 'integer'},required=True)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('order_id', type=int, location='args')
        parser.add_argument('Magic-key', type=int, location='headers')
        magic_key = parser.parse_args().get('Magic-key')
        if magic_key not in [1,2]:
            return Error.getError(401, "Unauthorized")

        order_id = parser.parse_args().get('order_id')
        
        order = OrderModel.query.filter_by(id=order_id).one_or_none()
        if order == None:
            return Error.getError(404, "Order not found")

        response = jsonify(order.serialize())
        response.status_code = 200
        return response


    @swagger.tags(['Zamówienia'])
    @swagger.reorder_with(OrderSchema, description="Post a order")
    @swagger.expected(OrderCreateSchema)   
    @swagger.parameter(_in='header', name='Magic-key', description='Magic key',schema={'type': 'integer'},required=True)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Magic-key', type=int, location='headers')
        magic_key = parser.parse_args().get('Magic-key')
        if magic_key not in [1,2]:
            return Error.getError(401, "Unauthorized")
        
        json = request.get_json()

        order = OrderModel()
        order.details = json['details']
        order.status_id  = json['status']
        
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
                return  Error.getError(500, "Error databse address... TMI")

        order.address = address

        user = UserModel.query.filter_by(id=json['orderedBy']).one_or_none()
        if user == None:
            return Error.getError(404, "User not found")

        order.ordered_by = [user]

        order.teas = []
        [order.teas.append(TeaModel.query.filter_by(id=tea_id).one_or_none()) for tea_id in  json['teaIds']]

        try:
            db.session.add(order)
            db.session.commit()
        except Exception:
            return Error.getError(500, "Internal server error i'm tired")


        response = jsonify(order.serialize())
        response.status_code = 200
        return response


    @swagger.tags(['Zamówienia'])
    @swagger.reorder_with(OrderStatusSchema, description="Change order status")
    @swagger.expected(OrderCreateSchema)   
    @swagger.parameter(_in='query', name='order_id', description='Order ID',schema={'type': 'integer'},required=True)
    @swagger.parameter(_in='header', name='Magic-key', description='Magic key',schema={'type': 'integer'},required=True)
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('order_id', type=int, location='args')
        parser.add_argument('Magic-key', type=int, location='headers')
        magic_key = parser.parse_args().get('Magic-key')
        if magic_key not in [1,2]:
            return Error.getError(401, "Unauthorized")

        order_id = parser.parse_args().get('order_id')

        order = OrderModel.query.filter_by(id=order_id).one_or_none()
        if order == None:
            return Error.getError(404, "Order not found")

        json = request.get_json()
        order.status_id  = json['status']
        
        try:
            db.session.add(order)
            db.session.commit()
        except Exception:
            return Error.getError(500, "Like others u know server database workin niht bleble")


        response = jsonify(order.serialize())
        response.status_code = 200
        return response

