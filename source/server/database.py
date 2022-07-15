import re


class Database:
    @staticmethod
    def create_tables(connection):
        connection.execute(
            """CREATE TABLE IF NOT EXISTS users (
                                        id integer,
                                        username text NOT NULL UNIQUE,
                                        password text,
                                        PRIMARY KEY (id));"""
        )
        connection.execute(
            """CREATE TABLE IF NOT EXISTS folders ( 
                                        owner integer NOT NULL,
                                        path text, 
                                        PRIMARY KEY (owner, path));"""
        )
        connection.execute(
            """CREATE TABLE IF NOT EXISTS files ( 
                                        owner integer NOT NULL,
                                        name text NOT NULL,
                                        folder text,
                                        hash text,
                                        PRIMARY KEY (owner, name, folder));"""
        )
        connection.commit()

    @staticmethod
    def seed_data(connection):
        connection.execute(
            "insert or ignore into users (username, password) values ('aaa', 'a')"
        )
        connection.execute(
            "insert or ignore into users (username, password) values ('bbb', 'b')"
        )
        connection.commit()

    @staticmethod
    def config(connection):
        connection.execute("PRAGMA foreign_keys = ON;")

        def regexp(expr, item):
            reg = re.compile(expr)
            return reg.search(item) is not None

        connection.create_function("REGEXP", 2, regexp)
        connection.commit()
