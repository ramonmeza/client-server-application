import collections
import struct


class ProtocolError(BaseException):
    pass


PROTOCOL_HEADER_SIZE: int = 5
Header = collections.namedtuple("Header", ["message_id", "num_data_bytes"])

Protocol = collections.namedtuple("Protocol", ["header", "data"])
"""
+--------+--------+---------------------------------+
| offset | type   | description                     |
+========+========+=================================+
| 0      | uint8  | message id                      |
+--------+--------+---------------------------------+
| 1      | uint32 | number of bytes in message data |
+--------+--------+---------------------------------+
| 5      | bytes  | message data                    |
+--------+--------+---------------------------------+
"""


def parse_protocol(data: bytes) -> Protocol:
    """get the protocol header values.

    Args:
        data (bytes): the data to parse

    Raises:
        ProtocolError: if there was an error getting the protocol header.

    Returns:
        tuple: (message_id: uint8, num_data_bytes: uint32, data_bytes: bytes)
    """
    try:
        header = Header(*struct.unpack("!BI", data[:PROTOCOL_HEADER_SIZE]))
        data = data[PROTOCOL_HEADER_SIZE : PROTOCOL_HEADER_SIZE + header.num_data_bytes]
        return Protocol(header, data)
    except:
        raise ProtocolError
