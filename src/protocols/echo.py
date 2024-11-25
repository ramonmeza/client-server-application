import collections
import struct

Echo = collections.namedtuple("Echo", ["text_length", "text"])


def parse_echo(data: bytes) -> Echo:
    (text_length,) = struct.unpack("!H", data[:2])
    text = str(data[2 : 2 + text_length], "utf-8")
    return Echo(text_length, text)
