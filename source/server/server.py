import os
import sqlite3
from datetime import datetime
from encryption import Encryption
from datetime import datetime
from database import Database
from exceptions import AlreadyExistsException


class Server:
    def __init__(self) -> None:
        self.encryption = Encryption()
        self.db_connection = sqlite3.connect("fylo.db")
        Database.config(self.db_connection)
        Database.create_tables(self.db_connection)
        Database.seed_data(self.db_connection)

    def login(self, username, timestamp):
        if (timestamp - datetime.now()).total_seconds() > 10:
            return
        user = self.db_connection.execute(
            "select * from users where username = ?", (username,)
        ).fetchone()
        return self.encryption.encrypt_token(
            {
                "id": user[0],
                "username": user[1],
                "timestamp": str(datetime.now()),
                "expire": 300,
            },
            user[2],
        )

    def make_directory(self, current_dir, new_dir, token):
        user_id = self.encryption.authenticate(token)
        new_path = os.path.join(current_dir, new_dir)
        try:
            self.db_connection.execute(
                "insert into folders (owner, path) values (?, ?)",
                (user_id, new_path),
            )
            self.db_connection.commit()
        except:
            raise AlreadyExistsException()

    def list_directory(self, dir, token):
        user_id = self.encryption.authenticate(token)
        path = os.path.join("/", dir)
        if path is "/":
            path = ""
        files = self.db_connection.execute(
            "select * from folders where owner = ? AND path REGEXP ?",
            (user_id, "^{0}/[^/]+$".format(path)),
        ).fetchall()
        return files

    def is_directory_valid(self, dir, sub_dir, token):
        user_id = self.encryption.authenticate(token)
        path = os.path.join(dir, sub_dir)
        path = os.path.normpath(path)
        entity = self.db_connection.execute(
            "select * from folders where owner = ? AND path = ?",
            (user_id, path),
        ).fetchone()
        return path is "/" or entity is not None
