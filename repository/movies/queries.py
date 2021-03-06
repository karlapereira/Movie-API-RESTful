from src.interfaces.db_connection_interface import DbConnectionInterface


def create_movie_table():
    sql = """
        CREATE TABLE IF NOT EXISTS movies( 
            "year" INT(1),
            "title" VARCHAR(36),
            "studios" VARCHAR(36),
            "producers" VARCHAR(36),
            "winner" TINYNT(1) DEFAULT 0
        )
    """

    return DbConnectionInterface().execute(sql)


def get_all_movies():
    sql = """
        SELECT 
            year,
            title,
            studios,
            producers,
            winner
            FROM movies;
    """

    return DbConnectionInterface().fetch_all(sql)


def get_producers_with_mult_winner_movies():
    sql = """
        SELECT M.producers FROM (
            SELECT COUNT(*) as winner_qtd, producers
                FROM movies
                WHERE winner="yes"
                GROUP BY producers
        ) M WHERE M.winner_qtd >= 2;
    """

    return DbConnectionInterface().fetch_all(sql)


def get_winner_movies_of_producers(winner_movies_producers):
    sql = """
        SELECT 
            m.producers,
            m.year
        FROM movies m
        WHERE m.producers IN ({}) 
            AND m.winner="yes"
        ORDER BY m.year ASC;
    """
    where_in_clause = ", ".join(["?"]*len(winner_movies_producers))

    sql = sql.format(where_in_clause)

    return DbConnectionInterface().fetch_all(sql, winner_movies_producers)


def delete_all_movies():
    sql = """
        DELETE FROM movies;
    """

    return DbConnectionInterface().execute(sql)
