import pandas as pd
from application.responses import ResponseCodes, ResponseFailure, ResponseSuccess, ResponseTypes

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
                ResponseCodes.SUCCESS
            )
        except Exception as exc:
            return ResponseFailure(
                ResponseTypes.BAD_REQUEST,
                {"message": f"Error: It's not possible to load the csv into a database: {exc[0]}"},
                ResponseCodes.BAD_REQUEST
            )
