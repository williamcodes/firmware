import logging

import serial

from . import common, xbee


def send(frame, xb):
    print('sending {:r}'.format(frame))
    xb.write(frame)
    print('sent')

@common.main
def main():
    with serial.Serial('/dev/ttyAMA0') as xb:
        logging.info('connected to xbee.')

        send(xbee.frame(b'\x08xAG\xFF\xFF'), xb)
        send(xbee.frame(b'\x08xSP\x05\x7A\x58'), xb)
        send(xbee.frame(b'\x08xWR'), xb)

