class Normalize:
    def normalize_movie(self, movies):
        movies_normalized = []
        for movie in movies:
            movies_normalized.append(
                {
                    "year":movie[0],
                    "title": movie[1],
                    "studios": movie[2],
                    "producers": movie[3],
                    "winner": movie[4]
                }
            )
        
        return movies_normalized