from flask_restx import fields

from application.server.instance import server


movie = server.api.model(
    "Movie",
    {
        "year": fields.String(required=True, max_length=4, default=""),
        "title": fields.String(required=True),
        "studios": fields.String(required=True),
        "producers": fields.String(required=True),
        "winner": fields.String(required=True, default=""),
    },
)

response_movies = server.api.model(
    "Movies",
    {
        "movies": fields.List(fields.Nested(movie))
    }
)

movie_range_by_producer = server.api.model(
    "movie_range_by_producer",
    {
        "producer": fields.String(required=True, default=""),
        "interval": fields.Integer(required=True, default=0),
        "previousWin": fields.Integer(required=True),
        "followingWin": fields.Integer(required=True),
    },
)

response_movies_with_max_ranges = server.api.model(
    "MoviesRangeIntervals",
    {
        "min": fields.List(fields.Nested(movie_range_by_producer)),
        "max": fields.List(fields.Nested(movie_range_by_producer))
    }
)
