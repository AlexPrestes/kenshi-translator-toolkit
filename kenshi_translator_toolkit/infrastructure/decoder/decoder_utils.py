import io
import logging
import os
import struct
from collections.abc import Callable
from typing import Any


def read_int(f: io.BytesIO) -> int:
    r_int = struct.unpack('<i', f.read(4))[0]
    logging.debug('read_int: %s', r_int)
    return r_int


def read_char(f: io.BytesIO) -> int:
    r_char = struct.unpack('<b', f.read(1))[0]
    logging.debug('read_char: %s', r_char)
    return r_char


def read_uchar(f: io.BytesIO) -> int:
    r_uchar = struct.unpack('<B', f.read(1))[0]
    logging.debug('read_uchar: %s', r_uchar)
    return r_uchar


def read_float(f: io.BytesIO) -> float:
    r_float = struct.unpack('<f', f.read(4))[0]
    logging.debug('read_float: %s', r_float)
    return r_float


def read_bool(f: io.BytesIO) -> bool:
    r_bool = f.read(1)[0] != 0
    logging.debug('read_bool: %s', r_bool)
    return r_bool


def read_string(f: io.BytesIO) -> str:
    MAX_STRING_LENGTH = 15 * 1024 * 1024
    length = read_int(f)
    if not (0 <= length < MAX_STRING_LENGTH):
        logging.warning(
            'String length inválido (%s), ignorando...', length
        )
        try:
            f.seek(length, os.SEEK_CUR)
        except Exception as e:
            logging.warning('Erro ao pular string: %s', e)
        return ''
    try:
        r_string = f.read(length).decode('utf-8', errors='replace')
        logging.debug('read_string: %s', r_string)
        return r_string
    except Exception as e:
        logging.warning('Erro ao ler string (%s): %s', length, e)
        return ''


def skip_block(f: io.BytesIO, read_func: Callable[[io.BytesIO], Any]
):
    logging.debug('Initializing skip_block')
    s_count = read_int(f)
    for _ in range(s_count):
        read_string(f)
        read_func(f)
    logging.debug('Finalizing skip_block')


def skip_vector_block(f: io.BytesIO, num: int):
    logging.debug('Initializing skip_vector_block')
    sv_count = read_int(f)
    for _ in range(sv_count):
        read_string(f)
        for _ in range(num):
            read_float(f)
    logging.debug('Finalizing skip_vector_block')
