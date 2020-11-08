from app_models.tea_model import TeaModel
from flask import Response, abort, jsonify, request
from flask_restful_swagger_3 import Resource, swagger
from flask_restful import reqparse
from app_models.order_model import OrderModel, OrderSchema, OrderCreateSchema
from app_models.address_model import AddressModel
from app_models.user_model import UserModel
from app import db

class OrderRes(Resource):
    @swagger.tags(['Zamówienia'])
    @swagger.reorder_with(OrderSchema, description="Returns a order")    
    @swagger.parameter(_in='query', name='order_id', description='Order ID',schema={'type': 'integer'},required=True)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('order_id', type=int, location='args')
        order_id = parser.parse_args().get('order_id')
        
        order = OrderModel.query.filter_by(id=order_id).one_or_none()
        if order == None:
            return "toDoblald"

        response = jsonify(order.serialize())
        response.status_code = 200
        return response


    @swagger.tags(['Zamówienia'])
    @swagger.reorder_with(OrderSchema, description="Post a order")
    @swagger.expected(OrderCreateSchema)   
    def post(self):
        json = request.get_json()

        order = OrderModel()
        order.details = json['details']
        order.status  = json['status']
        
        address = AddressModel()
        json_address = json['address']
        if 'id' in json_address:
            address = AddressModel.query.filter_by(id=json_address['id']).one_or_none()
            if address == None:
                return "toDoblald1"
        else:
            address.number = json_address['number']
            address.city = json_address['city']
            address.country = json_address['country']
            address.street = json_address['street']
            address.postal_code = json_address['postal_code']
            try:
                db.session.add(address)
            except Exception:
                return "toDoblald2"

        order.address = address

        user = UserModel.query.filter_by(id=json['orderedBy']).one_or_none()
        if user == None:
            return "toDoblald"

        order.ordered_by = [user]

        order.teas = []
        [order.teas.append(TeaModel.query.filter_by(id=tea_id).one_or_none()) for tea_id in  json['teaIds']]

        try:
            db.session.add(order)
            db.session.commit()
        except Exception:
            return "toDoblald3"


        response = jsonify(order.serialize())
        response.status_code = 200
        return response

