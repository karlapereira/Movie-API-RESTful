


from src.domain.use_cases.movie import Movie


class MovieInterface:
    def __init__(self):
        self._movie = Movie()

    def insert_csv_into_database(self, csv):
        return self._movie.insert_csv_into_database(csv)
