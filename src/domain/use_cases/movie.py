import pandas as pd

from application.responses import ResponseCodes, ResponseFailure, ResponseSuccess, ResponseTypes
from constants import MAX_RANGE, MIN_RANGE
from src.domain.normalize.normalize import Normalize
from repository.movies import  queries
from src.interfaces.db_connection_interface import DbConnectionInterface

class Movie:
    def __init__(self):
        self.db_connection = DbConnectionInterface().db_connection.con

    def insert_csv_into_database(self, csv):
        df = pd.read_csv(csv, sep=';')
        try:
            result = df.to_sql("movies", self.db_connection, if_exists='append', index=False)
            return ResponseSuccess(
                {"message": f"Success: CSV load into database. Inserted {result} new data."},
                ResponseCodes.CREATED
            )
        except Exception as exc:
            return ResponseFailure(
                ResponseTypes.BAD_REQUEST,
                {"message": f"Error: It's not possible to load the csv into a database: {exc[0]}"},
                ResponseCodes.BAD_REQUEST
            )

    def get_all_movies(self):
        movies = queries.get_all_movies()

        if movies:
            normalized_movie = {"movies": Normalize().normalize_movie(movies)}
            return ResponseSuccess(
                normalized_movie,
                ResponseCodes.SUCCESS
            )

        return ResponseSuccess(
            {},
            ResponseCodes.NOT_FOUND
        )

    def get_range_intervals_winner_producers(self):
        range_winner_movies = {
            "min": [],
            "max": []
        }

        producers_with_winner_movies = queries.get_producers_with_mult_winner_movies()
        if producers_with_winner_movies:
            producers_with_winner_movies = [producer[0] for producer in producers_with_winner_movies]
            winner_movies_producers = queries.get_winner_movies_of_producers(producers_with_winner_movies)
            if winner_movies_producers:
                interval_winner_movies = self.calculate_interval_of_winner_movie(winner_movies_producers)
                if interval_winner_movies:
                    min_interval_winner_producers = self.get_min_range_winner_producers(interval_winner_movies)
                    max_interval_winner_producers = self.get_max_range_winner_producers(interval_winner_movies)

                    range_winner_movies["min"] = min_interval_winner_producers
                    range_winner_movies["max"] = max_interval_winner_producers

                    return ResponseSuccess(
                        range_winner_movies,
                        ResponseCodes.SUCCESS
                    )

        return ResponseSuccess(
                range_winner_movies,
                ResponseCodes.NOT_FOUND
            )

    def calculate_interval_of_winner_movie(self, winner_movies_producers):
        interval_winner_movies = {}

        for movie in winner_movies_producers:
            if movie[0] not in interval_winner_movies:
                interval_winner_movies[movie[0]] = {
                    "producer": movie[0],
                    "max_interval":-1,
                    "previousWin": -1,
                    "followingWin": -1,
                    "movie_years": [],
                    "winner_movies_intervals": {}
                }
            interval_winner_movies[movie[0]]["movie_years"].append(
                movie[1]
            )

        if interval_winner_movies:
            for producer in interval_winner_movies:
                for movie_year in interval_winner_movies[producer]["movie_years"]:
                    producer_dict = interval_winner_movies[producer]
                    if producer_dict["max_interval"] == -1:
                        producer_dict["previousWin"] = movie_year
                        producer_dict["followingWin"] = -1
                        producer_dict["max_interval"] = 0
                        continue

                    producer_dict["followingWin"] = movie_year
                    producer_interval = producer_dict["followingWin"] - producer_dict["previousWin"]

                    if not producer_interval in producer_dict["winner_movies_intervals"]:
                        producer_dict["winner_movies_intervals"][producer_interval] = []
                    
                    producer_dict["winner_movies_intervals"][producer_interval].append(
                        {
                            "producer": producer,
                            "interval": producer_interval,
                            "previousWin": producer_dict["previousWin"],
                            "followingWin": producer_dict["followingWin"]
                        }
                    )
                    
                    if producer_dict["max_interval"] <= producer_interval <= MAX_RANGE  or producer_dict["max_interval"] == 0:
                        producer_dict["max_interval"] = producer_interval

                    producer_dict["previousWin"] = movie_year

        return interval_winner_movies

    def get_max_range_winner_producers(self, interval_winner_movies):
        max_interval = None
        max_range_winner_producer = []

        for producer in interval_winner_movies:
            producer_dict = interval_winner_movies[producer]
            if not max_interval:
                max_interval = producer_dict["max_interval"]
                continue

            if producer_dict["max_interval"] > max_interval:
                max_interval = producer_dict["max_interval"]

        if max_interval:
            for producer in interval_winner_movies:
                if max_interval in interval_winner_movies[producer]["winner_movies_intervals"]:
                    max_range_winner_producer += interval_winner_movies[producer]["winner_movies_intervals"][max_interval]

        return max_range_winner_producer

    def get_min_range_winner_producers(self, interval_winner_movies):
        min_range_winner_producer = []

        for producer in interval_winner_movies:
            if MIN_RANGE in interval_winner_movies[producer]["winner_movies_intervals"]:
                min_range_winner_producer += interval_winner_movies[producer]["winner_movies_intervals"][MIN_RANGE]

        return min_range_winner_producer

    def delete_all_movies(self):
        queries.delete_all_movies()
        return ResponseSuccess(
            {"message": "data from movies table was deleted!"},
            ResponseCodes.SUCCESS
        )
