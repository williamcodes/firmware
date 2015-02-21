import logging
import sys
import time

import serial

from . import common


def main(device='/dev/ttyAMA0'):
    with serial.Serial(device) as xbee:
        logging.info('connected to xbee.')

        cmd = b'\x08zAG\xFF\xFF'
        msg = b'\x7E' + bytes([0, len(cmd)]) + cmd + bytes([0xFF - common.checksum(cmd)])

        print('sending {}'.format(repr(msg)))
        xbee.write(msg)
        print('sent')
        
        while True:
            print(repr(xbee.read(1)))
            time.sleep(0.1)

if __name__ == '__main__':
    logging.info('starting...')
    main(sys.argv[1])
