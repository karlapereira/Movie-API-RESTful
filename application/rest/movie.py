import json

from flask import Response, request
from flask_restx import Resource, reqparse
from werkzeug.datastructures import FileStorage

from application.responses import ResponseCodes, ResponseFailure, ResponseTypes
from application.server.instance import server
from application.schemas.models.response_movies_model import response_movies_with_max_ranges, response_movies
from constants import DATABASE_CSV
from src.interfaces.movie_interface import MovieInterface


movie = server.movie
params = {
    "producers_range_winner": "Return a list min and max of producers with range interval of winner movies"
}

upload_parser = reqparse.RequestParser()
upload_parser.add_argument(
    'database_csv', 
    location='files',
    type=FileStorage, 
    required=True, 
    action="append"
)


@movie.route("/movie", methods=["POST", "GET"])
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
            data = request.files[DATABASE_CSV]
            response = MovieInterface().insert_csv_into_database(data)

            return Response(
                json.dumps(response.value["response"]),
                mimetype=mimetype,
                status=response.value["status_code"]
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

    @movie.response(200, "Success with query param", response_movies_with_max_ranges)
    @movie.response(200, "Success", response_movies)
    @movie.doc(params=params)
    def get(self):
        mimetype="application/json"
        if not request:
            pass
        try:
            query_param = request.args.get("producers_range_winner")

            if query_param:
                if query_param.lower() == "true":
                    response = MovieInterface().get_intervals_winner_producers()

                    return Response(
                        json.dumps(response.value["response"]),
                        mimetype=mimetype,
                        status=response.value["status_code"]
                    )

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
