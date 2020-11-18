from __future__ import annotations
from typing import NewType
from CipherText import CipherText
from Histogram import Histogram

HexStr = NewType('HexStr', str)
Key = NewType('Key', str)
Plaintext = NewType('Plaintext', str)


def simple_filter(data: bytes) -> bool:
    bytes_above_128 = filter(lambda x: x > 128, data)
    if any(bytes_above_128):
        return True
    return False


def xor_scan(data: CipherText) -> list[tuple[CipherText, int]]:
    byte_len = len(data)
    raw_xors = []
    for i in range(256):
        deciphered = data ^ i
        if simple_filter(deciphered.get_bytes()):
            continue

        raw_xors.append((deciphered, i))

    return raw_xors


def scan_and_sort(target: CipherText, len: int = 5):
    items = xor_scan(target)
    histogram = Histogram(mode="ENGLISH")
    scored_items = sorted(items, key=lambda x: histogram.score(x[0].get_bytes()))
    return scored_items[:len]
