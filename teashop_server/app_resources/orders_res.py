from flask import Response, abort, jsonify, request
from flask_restful_swagger_3 import Resource, swagger
from flask_restful import reqparse
from app_models.order_model import OrderModel, OrderPaginated
from app_models.user_model import UserModel
from app import db
from sqlalchemy import or_, and_, desc

class OrdersRes(Resource):
    @swagger.tags(['Zamówienia'])
    @swagger.reorder_with(OrderPaginated, description="Finds all maching orders")    
    @swagger.parameter(_in='query', name='orderedBy', description='Tea Name',schema={'type': 'integer'},required=True)
    @swagger.parameter(_in='query', name='perPage', description='Number of teas per page',schema={'type': 'integer'},required=True)
    @swagger.parameter(_in='query', name='pageNumber', description='Page number',schema={'type': 'integer'},required=True)
    @swagger.parameter(_in='query', name='sortBy', description='Sort teas by',schema={'type': 'string'},required=False)
    @swagger.parameter(_in='query', name='sortDirection', description='Sorts Direction',schema={'type': 'string'},required=False)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('orderedBy', type=int, location='args')
        parser.add_argument('pageNumber', type=int, location='args')
        parser.add_argument('sortBy', type=str, location='args')
        parser.add_argument('sortDirection', type=str, location='args')

        ordered_by_id = parser.parse_args().get('orderedBy')
        per_page = parser.parse_args().get('perPage')
        page_number = parser.parse_args().get('pageNumber')
        sort_by = parser.parse_args().get('sortBy')
        sort_dir = parser.parse_args().get('sortDirection') if parser.parse_args().get('sortDirection') in ['inc', 'desc'] else 'inc'

        ordered_by = UserModel.query.filter_by(id=ordered_by_id).one_or_none()
        if ordered_by == None:
            return "toDoblald"

        order_name = {
            'id' : OrderModel.id,
            'status' : OrderModel.status,
        }

        order_query = None
        if sort_by in order_name:
            order_query = {
                'inc' : order_name[sort_by],
                'desc' : desc(order_name[sort_by])
            }[sort_dir]

        orders_paginator = OrderModel.query.filter(OrderModel.ordered_by.contains(ordered_by)) \
            .order_by(order_query) \
            .paginate(page=page_number, per_page=per_page, error_out=False, max_per_page=1500)

        orders = []
        [orders.append(order.serialize()) for order in orders_paginator.items]

        resDic = {'page' : orders_paginator.page,
                  'pages': orders_paginator.pages,
                  'perPage': orders_paginator.per_page,
                  'hasNext': orders_paginator.has_next,
                  'hasPrev': orders_paginator.has_prev,
                  'total': orders_paginator.total,
                  'itemsNumber': len(orders),
                  'items': orders
                }

        response = jsonify(resDic)
        response.status_code = 200
        return response