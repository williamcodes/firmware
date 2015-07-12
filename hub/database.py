import time

import sqlite3


class Database:
    def __enter__(self):
        self.db = sqlite3.connect('heatseeknyc.db')
        self.db.__enter__()
        return _Database(self.db)

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.__exit__(exc_type, exc_value, traceback)
        self.db.close()

class _Database:
    def __init__(self, db):
        self.db = db

    def insert_reading(self, cell_id, temperature):
        with self.db as db:
            db.execute('insert into readings values (?, ?, ?)',
                       (cell_id, round(time.time()), temperature))

    def get_untransmitted_readings(self):
        with self.db as db:
            (reading_id,), = db.execute('select reading_id from transmitted')
            return db.execute('select rowid, * from readings where rowid > ?', (reading_id,))

    def set_transmitted_readings(self, reading_id):
        with self.db as db:
            db.execute('update transmitted set reading_id = ?', (reading_id,))
