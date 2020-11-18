from __future__ import annotations
from typing import Union
import binascii
import itertools


class CipherText:
    data: bytes

    def __init__(self, data: bytes):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __xor__(self, other: Union[CipherText, int]):
        if isinstance(other, CipherText):
            key = itertools.cycle(other.data)
        elif isinstance(other, int):
            key = itertools.repeat(other)
        else:
            raise TypeError("Unsupported parameter type")

        items = zip(self.data, key)
        return CipherText(bytes(map(lambda x: x[0] ^ x[1], items)))

    def __eq__(self, other: Union[str, CipherText]):
        if type(other) != str and type(other) != CipherText:
            raise TypeError("type(other) != str and type(other) != TextView")

        if type(other) == str:
            pair_bytes = zip(self.data, from_hexstr(other).data)
        else:
            pair_bytes = zip(self.data, other.data)

        return len(list(filter(lambda x: x[0] != x[1], pair_bytes))) == 0

    def get_ascii(self) -> str:
        return "".join(map(chr, self.data))

    def get_hexstr(self) -> str:
        return binascii.hexlify(self.data).decode('utf8')

    def get_bytes(self) -> bytes:
        return self.data


def from_ascii(ascii_data: str) -> CipherText:
    return CipherText(ascii_data.encode('utf8'))


def from_hexstr(hexstr: str) -> CipherText:
    return CipherText(binascii.unhexlify(hexstr))
