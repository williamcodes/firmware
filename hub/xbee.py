
START = 0x7E
BYTEORDER = 'big'


def checksum(bites):
    s = 0
    for byte in bites:
        s = (s + byte) & 0xFF
    return s

def int_from_bytes(bites):
    return int.from_bytes(bites, byteorder=BYTEORDER)

def int_to_bytes(n, length):
    return n.to_bytes(length, byteorder=BYTEORDER)

def frame(command):
    return (bytes((START,))
            + int_to_bytes(len(command), 2)
            + command
            + bytes((0xFF - checksum(command),)))
