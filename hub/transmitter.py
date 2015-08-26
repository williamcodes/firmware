import binascii
import logging
import time

import requests

from . import common, database


logging.basicConfig(level=logging.INFO)

READINGS_URI = 'http://relay.heatseeknyc.com/readings'

def transmit(db, xbee_id):
    for reading_id, cell_id, timestamp, temperature in db.get_untransmitted_readings():
        cell_id = common.hexlify(cell_id)
        data = dict(hub=xbee_id, cell=cell_id, time=timestamp, temp=temperature)
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
            xbee_id = db.get_xbee_id()
            if xbee_id: break
            logging.warn('waiting for xbee id to appear in db...')
            time.sleep(1)
        xbee_id = common.hexlify(xbee_id)

        while True:
            transmit(db, xbee_id)
            time.sleep(1)
