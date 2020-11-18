from __future__ import annotations
from typing import NewType
from collections.abc import Sequence, Iterable
from CipherText import CipherText
from Histogram import Histogram
from functools import singledispatch
import multiprocessing

HexStr = NewType('HexStr', str)
Key = NewType('Key', str)
Plaintext = NewType('Plaintext', str)


def __simple_filter(data: bytes) -> bool:
    bytes_above_128 = filter(lambda x: x > 128, data)
    if any(bytes_above_128):
        return True
    return False


def _xor_scan(data: CipherText) -> list[tuple[CipherText, int]]:
    raw_xors = []
    for i in range(256):
        deciphered = data ^ i
        if __simple_filter(deciphered.get_bytes()):
            continue

        raw_xors.append((deciphered, i))

    return raw_xors


@singledispatch
def recover_plaintext(data, return_len: int = 5):
    raise TypeError("Unknown parameter type: {0}".format(type(data)))


@recover_plaintext.register
def _(data: CipherText, return_len: int = 5):
    items = _xor_scan(data)
    histogram = Histogram(mode="ENGLISH")
    scored_items = sorted(items, key=lambda x: histogram.score(x[0].get_bytes()))
    return scored_items[:return_len]


@recover_plaintext.register(Iterable)
def _(data: Iterable[CipherText], return_len: int = 5) -> Sequence[tuple[CipherText, str]]:
    with multiprocessing.Pool() as pool:
        o = pool.map(recover_plaintext, data)

    flattened = []
    for sub_list in o:
        flattened.extend(sub_list)

    histogram = Histogram()
    sorted_items = sorted(flattened, key=lambda x: histogram.score(x[0].get_bytes()))

    return sorted_items[:return_len]