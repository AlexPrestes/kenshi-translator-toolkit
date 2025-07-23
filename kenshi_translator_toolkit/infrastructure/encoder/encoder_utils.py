import io
import logging
import struct


def write_int(f: io.BytesIO, v: int) -> None:
    w_int = struct.pack('<i', v)
    logging.debug('write_int: %s', w_int)
    f.write(w_int)


def write_char(f: io.BytesIO, v: int) -> None:
    w_char = struct.pack('<b', v)
    logging.debug('write_char: %s', w_char)
    f.write(w_char)


def write_uchar(f: io.BytesIO, v: int) -> None:
    w_uchar = struct.pack('<B', v)
    logging.debug('write_uchar: %s', w_uchar)
    f.write(w_uchar)


def write_float(f: io.BytesIO, v: float) -> None:
    w_float = struct.pack('<f', v)
    logging.debug('write_float: %s', w_float)
    f.write(w_float)


def write_bool(f: io.BytesIO, v: bool) -> None:
    w_bool = struct.pack('<B', 1 if v else 0)
    logging.debug('write_bool: %s', w_bool)
    f.write(w_bool)


def write_string(f: io.BytesIO, v: str) -> None:
    w_str = v.encode('utf-8')
    write_int(f, len(w_str))
    logging.debug('write_string: %s', w_str)
    f.write(w_str)
