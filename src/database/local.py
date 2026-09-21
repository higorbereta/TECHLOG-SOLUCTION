import sqlite3
from contextlib import contextmanager

class LocalDatabase():
    def __init__(self, db_file):
        self.db_file = db_file

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self.db_file)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def initialize(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL,
                    telefone TEXT NOT NULL
                )
            ''')
            conn.commit()