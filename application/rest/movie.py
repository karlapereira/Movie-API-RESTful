import json

from flask import Response, request
from flask_restx import Resource, reqparse
from werkzeug.datastructures import FileStorage

from application.responses import ResponseCodes, ResponseFailure, ResponseTypes
from application.server.instance import server
from application.schemas.models.response_movies_model import response_movies
from constants import DATABASE_CSV
from src.interfaces.movie_interface import MovieInterface


movie = server.movie

upload_parser = reqparse.RequestParser()
upload_parser.add_argument(
    'database_csv', 
    location='files',
    type=FileStorage, 
    required=True, 
    action="append"
)


@movie.route("/movie", methods=["POST", "GET", "DELETE"])
@movie.response(400, "Invalid Parameter(s)")
@movie.response(404, "Not found data")
@movie.response(503, "Service Unavailable")
class Movie(Resource):
    @movie.response(200, {"message": "Success: CSV load into database. Inserted X new data."})
    @movie.expect(upload_parser)
    def post(self):
        mimetype="application/json"
        if not request:
            pass
        try:
            if DATABASE_CSV in request.files:
                data = request.files[DATABASE_CSV]
                if data.mimetype == "text/csv":
                    response = MovieInterface().insert_csv_into_database(data)

                    return Response(
                        json.dumps(response.value["response"]),
                        mimetype=mimetype,
                        status=response.value["status_code"]
                    )
        
            return Response(
                '{"Message": "Param required file .csv with key: database_csv"}',
                mimetype=mimetype,
                status=ResponseCodes.PARAMETERS_ERROR
            )

        except Exception as exc:
            response = ResponseFailure(
                ResponseTypes.SYSTEM_ERROR, 
                exc.args[0], 
                ResponseCodes.SYSTEM_ERROR
            )

            return Response(
                json.dumps(response.value["response"]),
                mimetype=mimetype,
                status=response.value["status_code"]
            )

    @movie.response(200, "Success", response_movies)
    def get(self):
        mimetype="application/json"
        if not request:
            pass
        try:
            response = MovieInterface().get_all_movies()

            return Response(
                json.dumps(response.message),
                mimetype=mimetype,
                status=response.status_code
            )

        except Exception as exc:
            response = ResponseFailure(
                ResponseTypes.SYSTEM_ERROR, 
                exc.args[0], 
                ResponseCodes.SYSTEM_ERROR
            )

            return Response(
                json.dumps(response.value["response"]),
                mimetype=mimetype,
                status=response.value["status_code"]
            )

    @movie.response(200, "Success", response_movies)
    def delete(self):
        mimetype="application/json"
        if not request:
            pass
        try:
            response = MovieInterface().delete_all_movies()

            return Response(
                json.dumps(response.message),
                mimetype=mimetype,
                status=response.status_code
            )

        except Exception as exc:
            response = ResponseFailure(
                ResponseTypes.SYSTEM_ERROR, 
                exc.args[0], 
                ResponseCodes.SYSTEM_ERROR
            )

            return Response(
                json.dumps(response.value["response"]),
                mimetype=mimetype,
                status=response.value["status_code"]
            )
