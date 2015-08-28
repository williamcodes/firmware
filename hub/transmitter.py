import logging
import time

import requests

from . import common, database


logging.basicConfig(level=logging.INFO)

READINGS_URI = 'http://relay.heatseeknyc.com/readings'

def transmit(db):
    for row in db.get_unrelayed_temperatures():
        id, xbee_id, cell_id, temperature, sleep_period, timestamp = row
        xbee_id = common.hexlify(xbee_id)
        cell_id = common.hexlify(cell_id)
        data = dict(hub=xbee_id, cell=cell_id, temp=temperature, sp=sleep_period, time=timestamp)
        logging.info(data)
        response = requests.post(READINGS_URI, data)
        if response.status_code == 200: db.set_relayed_temperature(id)
        else: logging.error('bad response: %s', response)
        time.sleep(1)

@common.main
@common.forever
def main():
    with database.Database() as db:
        logging.info('connected to database.')
        while True:
            transmit(db)
            time.sleep(1)
