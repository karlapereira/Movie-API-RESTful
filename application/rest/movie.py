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
            data = request.files[DATABASE_CSV]  # pass the form field name as key
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
