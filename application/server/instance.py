from flask import Flask, Blueprint, g
from flask_restx import Api
from repository.db_connection import DbConnection
# from ma import ma
# from db import db
from repository.movies import queries


class Server(object):
    def __init__(self):
        self.app = Flask(__name__)
        self.bluePrint = Blueprint('api', __name__, url_prefix='/api')
        self.api = Api(self.bluePrint, doc='/doc', title='API RESTfull of movies with Flask-Restx')
        self.app.register_blueprint(self.bluePrint)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['PROPAGATE_EXCEPTIONS'] = True
        self.app.config['JSON_SORT_KEYS'] = False


        #self.api.init_app(self.blueprint)
        
        self.movie = self.movie()


    def movie(self, ):
        return self.api.namespace(
            name='Movies', 
            description='Route for movies', 
            path='/'
        )

    def run(self, ):
        self.app.run(
            port=5000,
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
