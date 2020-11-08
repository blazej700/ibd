import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(basedir, 'app_db.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class SwaggerConfig(object):
    TITLE ="Sklepiczek z herbacikami"
    DESCRIPTION="Guys that\'s the best shop with herbatki ^^. OMG OMG to API pozwala na wszystko, u know! W postach nie podawać IDków!!!"
    VERSION="0.0.1"
    SWAGGER_URL = '/api/doc'
    API_URL = 'swagger.json'
        