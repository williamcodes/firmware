import logging
from struct import Struct

import serial

from . import common, database


logging.basicConfig(level=logging.INFO)

SHORT = Struct('>H') # big endian unsigned short
INT = Struct('>I') # big endian unsigned int


def listen(xbee, db):
    while xbee.read(1) != b'\x7E':
        logging.warn('expected frame start byte 0x7E but got {:02X}'.format(frame_start))

    length, = SHORT.unpack(xbee.read(2))

    frame = xbee.read(length + 1) # frame plus checksum byte

    checksum = common.checksum(frame)
    if checksum != 0xFF:
        raise Exception('expected frame plus checksum to be 0xFF but got {:02X}'.format(checksum))

    if frame[0] == 0x88: # AT Command Response
        command = frame[2:2+2]
        status = frame[4]
        data = frame[5:length]

        if status != 0:
            logging.warn('AT{} failed with status {}'.format(command, status))
        elif command in (b'SH', b'SL'):
            if len(data) != 4:
                raise Exception('AT{} response should be 4 bytes, but was {}'
                                .format(command, repr(data)))
            if command == b'SH': db.set_xbee_id_high(data)
            else: db.set_xbee_id_low(data)
        else:
            logging.info('unhandled AT{} response'.format(command))

    elif frame[0] == 0x92: # Data Sample Rx Indicator
        # TODO properly handle digital and analog masks
        if length != 18:
            raise Exception('expected length of 18 for 0x92 frame with one sample, but got {}'
                            .format(length))
        cell_id = frame[1:1+8]
        adc, = SHORT.unpack(frame[16:16+2])

        voltage = adc / 0x3FF * 3.3 # on Xbee, 0x3FF (highest value on a 10-bit ADC) corresponds to 3.3V...ish
        celsius = (voltage - 0.5) / 0.01 # on MCP9700A, 0.5V is 0°C, and every 0.01V difference is 1°C difference
        fahrenheit = celsius * (212 - 32) / 100 + 32

        logging.info('cell_id={} adc=0x{:x} voltage={:.2f} celsius={:.2f} fahrenheit={:.2f}'
                     .format(cell_id, adc, voltage, celsius, fahrenheit))

        # our resolution ends up being about 0.6°F, so we round to 1 decimal place:
        db.insert_reading(cell_id, round(fahrenheit, 1))

    else:
        logging.warn('unexpected frame type {:02X}'.format(frame[0]))

@common.main
@common.forever
def main():
    with serial.Serial('/dev/ttyAMA0') as xbee, database.Database() as db:
        logging.info('connected to xbee and database.')
        while True:
            listen(xbee, db)
