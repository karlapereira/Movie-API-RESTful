from repository.db_connection import DbConnection


class DbConnectionInterface:
    def __init__(self):
        self.db_connection = DbConnection()

    def execute(self, sql):
        return self.db_connection.execute(sql)

    def fetch_one(self, sql, mapping={}):
        return self.db_connection.fetch_one(sql, mapping)

    def fetch_all(self, sql, mapping={}):
        return self.db_connection.fetch_all(sql, mapping)
