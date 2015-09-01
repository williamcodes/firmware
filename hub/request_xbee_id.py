import logging

import serial

from . import common, xbee


def send(frame, xb):
    print('sending {}'.format(frame))
    xb.write(frame)
    print('sent')

@common.main
def main():
    with serial.Serial('/dev/ttyAMA0') as xb:
        logging.info('connected to xbee.')
        send(xbee.frame(b'\x08xSH'), xb)
        send(xbee.frame(b'\x08xSL'), xb)
