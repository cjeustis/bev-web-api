import logging.config
from flask import Flask, Blueprint
from src import settings
from src.api.users.endpoints.users import ns as users_namespace
from src.api.restplus import api
from src.database import db, reset_database, init_database

app = Flask(__name__)
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)


def configure_app(flask_app):
  flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
  flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
  flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
  flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
  flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
  flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
  flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
  flask_app.config['SECRET_KEY'] = settings.SECRET_KEY
  
  # Need to add CORS; throw in a couple extra headers while we are at it
  @flask_app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

def initialize_app(flask_app):
  configure_app(flask_app)
  blueprint = Blueprint('api', __name__, url_prefix='/api')
  api.init_app(blueprint)

  # Add endpoint namespaces here so we can navigate to them in a browser 
  api.add_namespace(users_namespace)
  # api.add_namespace(recipes_namespace)

  flask_app.register_blueprint(blueprint)
  db.init_app(flask_app)
  with app.app_context():
    db.create_all()
    # init_database()


def main():
  initialize_app(app)
  log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
  app.run(debug=settings.FLASK_DEBUG)

if __name__ == "__main__":
  main()
