import json

from flask import Response, request
from flask_restx import Resource

from application.responses import ResponseCodes, ResponseFailure, ResponseTypes
from application.server.instance import server
from application.schemas.models.response_movies_model import response_movies_with_max_ranges
from src.interfaces.movie_interface import MovieInterface


award_range = server.award_range


@award_range.route("/award-range", methods=["GET"])
@award_range.response(400, "Invalid Parameter(s)")
@award_range.response(404, "Not found data")
@award_range.response(503, "Service Unavailable")
@award_range.response(200, "Success with query param", response_movies_with_max_ranges)
class AwardRange(Resource):
    def get(self):
        mimetype="application/json"
        if not request:
            pass
        try:

            response = MovieInterface().get_intervals_winner_producers()

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
