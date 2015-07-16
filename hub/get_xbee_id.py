
import binascii

from . import common, database


@common.main
def main():
    with database.Database() as db:
        xbee_id = db.get_xbee_id()

    if xbee_id:
        print(binascii.hexlify(xbee_id).decode('ascii'))
