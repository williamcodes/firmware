import serial

def checksum(bs):
    for b in bs:
        

def main():
    with serial.Serial('/dev/ttyAMA0') as xbee:
        logging.info('connected to xbee.')
        frame = b'\x7E\x00\x04\x08\x00SP\x05\x7C\x4C'
        xbee.write(frame)
        xbee.write(checksum(frame))

if __name__ == '__main__':
    logging.info('starting...')
    main()
