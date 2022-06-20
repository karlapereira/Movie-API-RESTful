


from src.domain.use_cases.movie import Movie


class MovieInterface:
    def __init__(self):
        self._movie = Movie()

    def insert_csv_into_database(self, csv):
        return self._movie.insert_csv_into_database(csv)

    def get_intervals_winner_producers(self):
        return self._movie.get_range_intervals_winner_producers()

    def get_all_movies(self):
        return self._movie.get_all_movies()

    def delete_all_movies(self):
        return self._movie.delete_all_movies()
