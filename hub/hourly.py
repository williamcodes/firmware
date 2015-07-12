import logging
import sys
import time

import serial

from . import common

def send(command, xbee):
    frame = b'\x7E' + bytes([0, len(command)]) + command + bytes([0xFF - common.checksum(command)])
    print('sending {}'.format(repr(frame)))
    xbee.write(frame)
    print('sent')

@common.main
def main():
    with serial.Serial('/dev/ttyAMA0') as xbee:
        logging.info('connected to xbee.')

        send(b'\x08xAG\xFF\xFF', xbee)

        send(b'\x08xSP\x05\x7A\x58', xbee)
        send(b'\x08xWR', xbee)
