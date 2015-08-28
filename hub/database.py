
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

    def insert_temperature(self, xbee_id, cell_id, temperature, sleep_period):
        with self.db as db:
            db.execute('insert into temperatures (xbee_id, cell_id, temperature, sleep_period)'
                       ' values (?, ?, ?, ?)', (xbee_id, cell_id, temperature, sleep_period))

    def get_unrelayed_temperatures(self):
        with self.db as db:
            return db.execute('select rowid, xbee_id, cell_id, temperature, sleep_period, time'
                              ' from temperatures where relayed_time is null')

    def set_relayed_temperature(self, id):
        with self.db as db:
            db.execute('update temperatures set relayed_time = strftime("%s", "now")'
                       ' where rowid = ?', (id,))

    def get_xbee_id(self):
        with self.db as db:
            (high, low), = db.execute('select xbee_id_high, xbee_id_low from status')
        if high and low:
            return high + low  # concatenate byte strings

    def unset_xbee_id(self):
        with self.db as db:
            db.execute('update status set xbee_id_high = null, xbee_id_low = null')

    def set_xbee_id_high(self, high):
        with self.db as db:
            db.execute('update status set xbee_id_high = ?', (high,))

    def set_xbee_id_low(self, low):
        with self.db as db:
            db.execute('update status set xbee_id_low = ?', (low,))

    def get_sleep_period(self):
        with self.db as db:
            (sleep_period,), = db.execute('select sleep_period from status')
        return sleep_period

    def set_sleep_period(self, sleep_period):
        with self.db as db:
            db.execute('update status set sleep_period = ?', (sleep_period,))
