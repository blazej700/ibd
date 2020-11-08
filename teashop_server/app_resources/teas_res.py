from flask import Response, abort, jsonify, request
from flask_restful_swagger_3 import Resource, swagger
from flask_restful import reqparse
from app_models.tea_model import TeaModel, TeaPaginated
from sqlalchemy import or_, and_, desc
from app import db

class TeasRes(Resource):
    @swagger.tags(['Herbatka'])
    @swagger.reorder_with(TeaPaginated, description="Finds all maching teas")    
    @swagger.parameter(_in='query', name='name', description='Tea Name',schema={'type': 'string'},required=False)
    @swagger.parameter(_in='query', name='country', description='Country of origin of tea',schema={'type': 'string'},required=False)
    @swagger.parameter(_in='query', name='teaType', description='Type of tea',schema={'type': 'string'},required=False)
    @swagger.parameter(_in='query', name='minPrice', description='Minimal price of tea',schema={'type': 'integer'},required=False)
    @swagger.parameter(_in='query', name='maxPrice', description='Maximal price of tea',schema={'type': 'integer'},required=False)
    @swagger.parameter(_in='query', name='perPage', description='Number of teas per page',schema={'type': 'integer'},required=True)
    @swagger.parameter(_in='query', name='pageNumber', description='Page number',schema={'type': 'integer'},required=True)
    @swagger.parameter(_in='query', name='sortBy', description='Sort teas by',schema={'type': 'string'},required=False)
    @swagger.parameter(_in='query', name='sortDirection', description='Sorts Direction',schema={'type': 'string'},required=False)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='args')
        parser.add_argument('country', type=str, location='args')
        parser.add_argument('teaType', type=str, location='args')
        parser.add_argument('minPrice', type=int, location='args')
        parser.add_argument('maxPrice', type=int, location='args')
        parser.add_argument('perPage', type=int, location='args')
        parser.add_argument('pageNumber', type=int, location='args')
        parser.add_argument('sortBy', type=str, location='args')
        parser.add_argument('sortDirection', type=str, location='args')


        name = parser.parse_args().get('name') if parser.parse_args().get('name') != None else ''
        country = parser.parse_args().get('country') if parser.parse_args().get('country') != None else ''
        tea_type = parser.parse_args().get('teaType') if parser.parse_args().get('teaType') != None else ''
        min_price = parser.parse_args().get('minPrice') if parser.parse_args().get('minPrice') != None else 0
        max_price = parser.parse_args().get('maxPrice') if parser.parse_args().get('maxPrice') != None else 9999999999
        per_page = parser.parse_args().get('perPage')
        page_number = parser.parse_args().get('pageNumber')
        sort_by = parser.parse_args().get('sortBy')
        sort_dir = parser.parse_args().get('sortDirection') if parser.parse_args().get('sortDirection') in ['inc', 'desc'] else 'inc'


        order_name = {
            'id' : TeaModel.id,
            'name' : TeaModel.name,
            'price' : TeaModel.price,
            'country' : TeaModel.country,
            'teaType' : TeaModel.tea_type,
            'stock' : TeaModel.stock,
        }

        order_query = None
        if sort_by in order_name:
            order_query = {
                'inc' : order_name[sort_by],
                'desc' : desc(order_name[sort_by])
            }[sort_dir]

        
        teas_paginator = TeaModel.query \
        .filter(and_(TeaModel.name.like((name+'%')), 
                TeaModel.price>min_price,TeaModel.price<max_price), 
                TeaModel.country.like((country+'%')),
                TeaModel.tea_type.like((tea_type+'%'))) \
        .order_by(order_query) \
        .paginate(page=page_number, per_page=per_page, error_out=False, max_per_page=1500)

        teas = []
        [teas.append(tea.serialize()) for tea in teas_paginator.items]

        resDic = {'page' : teas_paginator.page,
                  'pages': teas_paginator.pages,
                  'perPage': teas_paginator.per_page,
                  'hasNext': teas_paginator.has_next,
                  'hasPrev': teas_paginator.has_prev,
                  'total': teas_paginator.total,
                  'itemsNumber': len(teas),
                  'items': teas
                }

        response = jsonify(resDic)
        response.status_code = 200
        return response