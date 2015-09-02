import logging

import serial

from . import common, database, xbee


logging.basicConfig(level=logging.INFO)


def listen(xb, db):
    while True:  # read until start byte
        b, = xb.read(1)
        if b == xbee.START: break
        logging.warn('expected start byte 0x%02X but got 0x%02X', xbee.START, b)
    length = xbee.int_from_bytes(xb.read(2))
    frame = xb.read(length)
    checksum, = xb.read(1)

    if xbee.checksum(frame) + checksum != 0xFF:
        raise Exception('frame checksum 0x%02X does not complement 0x%02X', xbee.checksum(frame), checksum)

    frame_type = frame[0]

    if frame_type == 0x88: # AT Command Response
        command = frame[2:4]
        status = frame[4]
        data = frame[5:]

        try: command = command.decode('ascii')
        except UnicodeDecodeError: pass

        if status != 0:
            logging.warn('AT%s failed with status %d', command, status)
        elif command in ('SH', 'SL'):
            if len(data) != 4:
                raise Exception('AT{} data should be 4 bytes, but was {}'.format(command, len(data)))
            if command == 'SH': db.set_xbee_id_high(data)
            else: db.set_xbee_id_low(data)
        elif command == 'SP' and data:
            if len(data) != 4:
                raise Exception('ATSP data should be 4 bytes, but was {}'.format(len(data)))
            db.set_sleep_period(xbee.int_from_bytes(data))
        else:
            logging.info('unhandled AT%s response', command)

    elif frame_type == 0x92: # Data Sample Rx Indicator
        # TODO properly handle digital and analog masks
        if len(frame) != 18:
            raise Exception('expected Rx frame with one sample to be 18 bytes, but was {}'.format(len(frame)))
        cell_id = frame[1:9]
        adc = xbee.int_from_bytes(frame[16:18])

        voltage = adc / 0x3FF * 3.3 # on Xbee, 0x3FF (highest value on a 10-bit ADC) corresponds to 3.3V...ish
        celsius = (voltage - 0.5) / 0.01 # on MCP9700A, 0.5V is 0°C, and every 0.01V difference is 1°C difference
        fahrenheit = celsius * (212 - 32) / 100 + 32

        logging.info('cell_id=%s adc=0x%x voltage=%.2f celsius=%.2f fahrenheit=%.2f',
                     cell_id, adc, voltage, celsius, fahrenheit)

        # our resolution ends up being about 0.6°F, so we round to 1 decimal place:
        db.insert_temperature(cell_id, round(fahrenheit, 1), db.get_sleep_period())

    else:
        logging.info('unhandled frame type 0x%02X', frame_type)


@common.main
@common.forever
def main():
    with serial.Serial('/dev/ttyAMA0') as xb, database.Database() as db:
        logging.info('connected to xbee and database.')
        while True:
            listen(xb, db)
