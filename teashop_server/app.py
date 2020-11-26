from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful_swagger_3 import Api, get_swagger_blueprint
from flask_swagger_ui import get_swaggerui_blueprint

from config import Config, SwaggerConfig
app = Flask(__name__)
app.config.from_object(Config)

api = Api(app, add_api_spec_resource=True, title=SwaggerConfig.TITLE, description=SwaggerConfig.DESCRIPTION, version=SwaggerConfig.VERSION)
db = SQLAlchemy(app)

from app_resources.user_res import UserRes
from app_resources.tea_res import TeaRes
from app_resources.teas_res import TeasRes
from app_resources.order_res import OrderRes
from app_resources.orders_res import OrdersRes
from app_resources.login_res import LoginRes
from app_resources.photo_res import TeaPhotoRes
from app_resources.dev_tool import DevTools

api.add_resource(UserRes, '/user')
api.add_resource(TeaRes, '/tea')
api.add_resource(TeasRes, '/teas')
api.add_resource(OrderRes, '/order')
api.add_resource(OrdersRes, '/orders')
api.add_resource(LoginRes, '/login')
api.add_resource(DevTools, '/dev')
api.add_resource(TeaPhotoRes, '/photo/<int:tea_id>')

db.create_all()
db.session.commit()

# TODO move this somewhere else
swagger_blueprint = get_swaggerui_blueprint(
    SwaggerConfig.SWAGGER_URL,
    SwaggerConfig. API_URL,
    config={'app_name': "Sklepiczek z herbatkami"})

app.register_blueprint(swagger_blueprint)


if __name__ == '__main__':
    app.run(debug=True)