import os
import sqlite3
from contextlib import closing
from typing import Optional


def get_all(query, **kwargs) -> [tuple]:
    with sqlite3.connect(os.environ.get("DATABASE_URL")) as connection:
        with closing(connection.cursor()) as cursor:
            for row in cursor.execute(query, kwargs).fetchall():
                yield row


def get_one(query, **kwargs) -> Optional[tuple]:
    with sqlite3.connect(os.environ.get("DATABASE_URL")) as connection:
        with closing(connection.cursor()) as cursor:
            row = cursor.execute(query, kwargs).fetchone()
            if row is None or row[0] is None:
                return None

            return row


def execute(query, **kwargs):
    with sqlite3.connect(os.environ.get("DATABASE_URL")) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(query, kwargs)
            connection.commit()
