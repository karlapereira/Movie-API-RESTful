from src.interfaces.db_connection_interface import DbConnectionInterface


def create_movie_table():
    sql = """
        CREATE TABLE IF NOT EXISTS movies(
            "id" INT(1), 
            "year" INT(1),
            "title" VARCHAR(36),
            "studios" VARCHAR(36),
            "producers" VARCHAR(36),
            "winner" TINYNT(1) DEFAULT 0,
            PRIMARY KEY (id)
        )
    """

    return DbConnectionInterface().execute(sql)


def insert_rows_into_movie_table(rows):
    sql = """
        INSERT INTO movies
            (year, title, title, studios, producers, winner)
        VALUES
            %(data)s
    """

    mapping = {"data": rows}

    return DbConnectionInterface().fetch_all(sql, mapping)


def get_producer_with_max_range_winner():
    sql = """
    """
    pass


def get_producer_with_more_fast_winner():
    sql = """
    """
    pass


def get_producer_with_min_range_winner():
    sql = """
    """
    pass


def get_producer_with_more_slow_winner():
    sql = """
    """
    pass
