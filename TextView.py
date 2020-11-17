from __future__ import annotations
from typing import Union, TypeVar, Sequence
#from collections.abc import Sequence
import binascii
import itertools

T = TypeVar('T')


def chunks(l: bytes, n: int) -> Sequence[bytes]:
    n = max(1, n)
    return [l[i:i+n] for i in range(0, len(l), n)]


class TextView:
    data: bytes

    def __init__(self, data: bytes):
        self.data = data

    def __len__(self):
        return len(self.data)

    def get_ascii(self) -> str:
        return "".join(map(chr, self.data))

    def get_hexstr(self) -> str:
        return binascii.hexlify(self.data).decode('utf8')

    def get_bytes(self) -> bytes:
        return self.data

    def __iter__(self):
        return iter(self.data)

    def __xor__(self, other: TextView):
        if type(other) != TextView:
            raise TypeError("type(other) != TextView")

        items = zip(self.data, itertools.cycle(other.data))
        return TextView(bytes(map(lambda x: x[0] ^ x[1], items)))

    def __eq__(self, other: Union[str, TextView]):

        if type(other) != str and type(other) != TextView:
            raise TypeError("type(other) != str and type(other) != TextView")

        if type(other) == str:
            pair_bytes = zip(self.data, from_hexstr(other).data)
        else:
            pair_bytes = zip(self.data, other.data)

        return len(list(filter(lambda x: x[0] != x[1], pair_bytes))) == 0


def from_ascii(ascii: str) -> TextView:
    return TextView(ascii.encode('utf8'))


def from_hexstr(hexstr: str) -> TextView:
    return TextView(binascii.unhexlify(hexstr))

if __name__ == "__main__":
    x = from_hexstr("1c0111001f010100061a024b53535009181c")
    y = from_hexstr("686974207468652062756c6c277320657965")
    assert(x ^ y == "746865206b696420646f6e277420706c6179")
