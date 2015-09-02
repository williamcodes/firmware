import argparse
import logging
import time

import serial

from . import common, xbee


def send(frame, xb):
    print('sending {}'.format(frame))
    xb.write(frame)
    print('sent')

@common.main
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('sleep_period', type=int)
    args = parser.parse_args()

    with serial.Serial('/dev/ttyAMA0') as xb:
        logging.info('connected to xbee.')

        # 'aggregate' all cells in default broadcast mode to point to us instead:
        # TODO do this more than once?
        send(xbee.frame(b'\x08xAG\xFF\xFF'), xb)
        time.sleep(0.1)

        # set sleep period, and write changes to persistent flash
        send(xbee.frame(b'\x08xSP' + xbee.int_to_bytes(args.sleep_period, 4)), xb)
        time.sleep(0.1)
        send(xbee.frame(b'\x08xWR'), xb)
        time.sleep(0.1)

        send(xbee.frame(b'\x08xSP'), xb)  # read new sleep period into db
