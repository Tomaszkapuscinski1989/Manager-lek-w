import sqlite3 as sq


class open_base:
    def __init__(self, nazwaBazy):
        self.nazwaBazy = nazwaBazy

    def __enter__(self):
        self.conn = sq.connect(self.nazwaBazy)
        self.c = self.conn.cursor()
        return self.c

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.conn.commit()
        self.conn.close()
