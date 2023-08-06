from contextlib import suppress
from sqlite3 import OperationalError, connect

from .auth import encodeUserPassword, decodeUserPassword


class CredentialsDatabase:
    def __init__(self, file: str = ":memory:") -> None:
        self.connection = connect(file)
        self.database = connect(file)

        with suppress(OperationalError):
            self.database.execute(
                "CREATE TABLE creds (%s varchar(32), %s varchar(32))" % self.columns
            )

    def __del__(self):
        self.connection.commit()
        self.connection.close()

    def __exit__(self, *err):
        del self

    def __enter__(self):
        return self.database

    def __contains__(self, key: object):
        return key in list(self.getUsers()) if isinstance(key, str) else False

    @property
    def columns(self):
        return ("Username", "Password")

    def put(self, user: str, passwd: str):
        self.database.execute(
            "INSERT INTO creds VALUES (?, ?)", (user, encodeUserPassword(passwd))
        )

    def get(self, user: str):
        for name, passwd in self.database.execute(
            "SELECT Username, Password FROM creds WHERE Username = ?", (user,)
        ):
            return name, decodeUserPassword(passwd)

    def getAll(self):
        for name, passwd in self.database.execute("SELECT Username, Password FROM creds"):
            yield str(name), decodeUserPassword(
                passwd
            )  #! "str(name)" really isn't necessary, its mostly for type hinting

    def getUsers(self):
        yield from self.database.execute("SELECT Username FROM creds")
