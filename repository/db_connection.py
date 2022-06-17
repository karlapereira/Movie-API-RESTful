import sqlite3

from constants import DATABASE


class DbSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        host = DATABASE
        if host not in cls._instances:
            cls._instances[host] = super(DbSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[host]


class DbConnection(metaclass=DbSingleton):
    def __init__(self, ):
        self.db = DATABASE
        self.con = None
        self.cur = None

    def connect(self):
        self.con = sqlite3.connect(self.db)
        return self.con

    def execute(self, sql, mapping={}):
        cur = self.con.cursor()
        cur.execute(sql, mapping)

    def fetch_all(self, sql, mapping={}):
        cur = self.con.cursor()
        cur.execute(sql, mapping)
        result = cur.fetchall()

        return result

    def fetch_one(self, sql, mapping={}):
        cur = self.con.cursor()
        cur.execute(sql, mapping)
        result = cur.fetchone()

        return result
