
BYTEORDER = 'big'
START = b'\x7E'
AT_TYPE = b'\x08'
DUMMY_ID = b'x'

def checksum(bites):
    s = 0
    for bite in bites:
        s = (s + bite) & 0xFF
    return s

def int_from_bytes(bites):
    return int.from_bytes(bites, byteorder=BYTEORDER)

def int_to_bytes(n, length):
    return n.to_bytes(length, byteorder=BYTEORDER)

def byte(b):
    return bytes((b,))

def frame(body):
    return (START
            + int_to_bytes(len(body), 2)
            + body
            + byte(0xFF - checksum(body)))

def at_frame(command, data=b''):
    return frame(AT_TYPE
                 + DUMMY_ID
                 + command.encode('ascii')
                 + data)
