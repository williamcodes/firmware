import functools
import logging
import re
import time


def checksum(frame):
    s = 0
    for byte in frame:
        s = (s + byte) & 0xFF
    return s

def forever(f):
    @functools.wraps(f)
    def g(*args, **kwargs):
        while True:
            try:
                f(*args, **kwargs)
            except Exception:
                logging.exception('error, retrying...')
                time.sleep(1)
    return g

def main(f):
    if f.__module__ == '__main__':
        logging.info('starting...')
        f()
    return f


_PI_ID_RE = re.compile(r'^Serial\s*: (\w*)')
def _get_pi_id():
    with open('/proc/cpuinfo') as f:
        for line in f:
            found = _PI_ID_RE.findall(line)
            if found: return found[0]
PI_ID = _get_pi_id() or 'unknown'
