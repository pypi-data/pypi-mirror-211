from typing import Literal

TYPE_BO = Literal['little', 'big']


def bytearr_byte(ba: bytearray) -> bytes:
    return bytes(ba)


def byte_bytearr(b: bytes) -> bytearray:
    return bytearray(b)


def strip_leading_null_bytes(b: bytes) -> bytes:
    ba = byte_bytearr(b)
    for idx, _b in enumerate(ba):
        if _b != 0:
            return bytearr_byte(ba[idx:])


def hex_byte(h: str, strip: bool = False) -> bytes:
    b = bytes.fromhex(h)

    if strip:
        return strip_leading_null_bytes(b)

    return b


def byte_int(b: bytes, bo: TYPE_BO = 'big') -> int:
    return int.from_bytes(b, bo)


def hex_int(h: str) -> int:
    return byte_int(hex_byte(h))


def int_byte(i: int, size: int = None, bo: TYPE_BO = 'big', strip: bool = True) -> bytes:
    if size is None:
        size = i.bit_length() + 7

    b = i.to_bytes(size, bo)

    if strip:
        return strip_leading_null_bytes(b)

    return b


def byte_hex(b: bytes) -> str:
    return b.hex()


def str_byte(s: str, enc: str = 'utf-8', strip: bool = False) -> bytes:
    b = s.encode(encoding=enc)

    if strip:
        return strip_leading_null_bytes(b)

    return b



def byte_str(b: bytes, enc: str = 'utf-8') -> str:
    return b.decode(encoding=enc)


def int_hex(i: int) -> str:
    return byte_hex(int_byte(i))
