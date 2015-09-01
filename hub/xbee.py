import struct


SHORT = struct.Struct('>H')  # big endian unsigned short

START = 0x7E


def checksum(bites):
    s = 0
    for byte in bites:
        s = (s + byte) & 0xFF
    return s

def frame(command):
    return (bytes((START,))
            + SHORT.pack(len(command))
            + command
            + bytes((0xFF - checksum(command),)))
