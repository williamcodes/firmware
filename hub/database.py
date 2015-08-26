import time

import sqlite3


class Database:
    def __enter__(self):
        self.db = sqlite3.connect('/home/pi/heatseeknyc.db')
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

    def get_xbee_id(self):
        with self.db as db:
            (high, low), = db.execute('select high, low from xbee_id')
        if high and low:
            return high + low

    def unset_xbee_id(self):
        with self.db as db:
            db.execute('update xbee_id set high = null, low = null')

    def set_xbee_id_high(self, high):
        with self.db as db:
            db.execute('update xbee_id set high = ?', (high,))

    def set_xbee_id_low(self, low):
        with self.db as db:
            db.execute('update xbee_id set low = ?', (low,))
