from __future__ import annotations
from typing import NewType
from CipherText import CipherText, from_ascii, from_hexstr
from Histogram import Histogram
import time

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
        # ih = hex(i)[2:]
        # key = "{0:02x}".format(i)
        deciphered = otp_xor(data, CipherText(bytes([i] * byte_len)))
        # if i == 118:
        #     print(deciphered.get_ascii())
        if simple_filter(deciphered.get_bytes()):
            continue

        raw_xors.append((deciphered, i))

    return raw_xors


def otp_xor(data: CipherText, key: CipherText) -> CipherText:
    return data ^ key


def scan_and_sort(target: CipherText, len: int = 5):
    items = xor_scan(target)
    histogram = Histogram(mode="ENGLISH")
    scored_items = sorted(items, key=lambda x: histogram.score(x[0].get_bytes()))
    return scored_items[:len]
