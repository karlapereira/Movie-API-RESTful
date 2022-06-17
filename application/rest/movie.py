import json

from flask import Response, request
from flask_restx import Resource
from application.responses import ResponseCodes, ResponseFailure, ResponseTypes

from application.server.instance import server
from constants import DATABASE_CSV
from src.interfaces.movie_interface import MovieInterface


movie = server.movie


@movie.route("/movie", methods=["POST", "GET"])
class Movie(Resource):
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
