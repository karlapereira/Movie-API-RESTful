from flask import Flask, Blueprint, g
from flask_restx import Api

from constants import SERVER_PORT, URL_PREFIX
from repository.db_connection import DbConnection
from repository.movies import queries


class Server(object):
    def __init__(self):
        self.app = Flask(__name__)
        self.blueprint = Blueprint('api', __name__, url_prefix=URL_PREFIX)
        self.app.config["RESTPLUS_MASK_SWAGGER"] = False
        self.api = Api(
            title="API Movies",
            description="Movies",
            version="1.0.0",
            contact="karlapereira@gec.com.br",
            default="Movies",
            doc="/docs"
        )
        self.app.config['JSON_SORT_KEYS'] = False
        self.api.init_app(self.blueprint)

        # namespaces
        self.movie = self.movie()

        self.app.register_blueprint(self.blueprint)


    def movie(self, ):
        return self.api.namespace(
            name='Movies', 
            description='Route for movies', 
            path='/'
        )

    def run(self, ):
        self.app.run(
            port=SERVER_PORT,
            debug=True,
            host='0.0.0.0'
        )


server = Server()
application = server.app


@application.before_first_request
def create_table_movie_if_not_exists():
    open_db_connection()
    queries.create_movie_table()


@application.before_request
def open_db_connection():
    g.db = DbConnection().connect()
