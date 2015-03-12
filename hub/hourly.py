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

def main():
    with serial.Serial('/dev/ttyAMA0') as xbee:
        logging.info('connected to xbee.')

        send(b'\x081AG\xFF\xFF', xbee)
        time.sleep(1)
        send(b'\x082SP\x05\x7A\x58', xbee)

if __name__ == '__main__':
    logging.info('starting...')
    main()
