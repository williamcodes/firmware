import binascii
import logging


def hexlify(bites):
    return binascii.hexlify(bites).decode('ascii')

def main(f):
    if f.__module__ == '__main__':
        logging.info('starting...')
        f()
    return f
