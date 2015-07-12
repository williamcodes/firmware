import logging
import time

import requests

from . import common, database


logging.basicConfig(level=logging.INFO)

READINGS_URI = 'http://relay.heatseeknyc.com/readings'
PI_ID = common.get_pi_id()

def transmit(db):
    for reading_id, cell_id, timestamp, temperature in db.get_untransmitted_readings():
        data = dict(hub=PI_ID, cell=cell_id, time=timestamp, temp=temperature)
        logging.info(data)
        response = requests.post(READINGS_URI, data)
        if response.status_code != 200: raise Exception('bad response: {}'.format(response))
        db.set_transmitted_readings(reading_id)
        time.sleep(1)

@common.main
@common.forever
def main():
    with database.Database() as db:
        logging.info('connected to database.')
        while True:
            transmit(db)
            time.sleep(1)
