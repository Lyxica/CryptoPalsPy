from __future__ import annotations
from typing import NewType
from CipherText import CipherText, from_ascii, from_hexstr
from Histogram import Histogram
import time

HexStr = NewType('HexStr', str)
Key = NewType('Key', str)
Plaintext = NewType('Plaintext', str)


def has_invalid_ascii(input: str) -> bool:
    return False
    for ch in input:
        if ch == '\n':
            continue
        if ch == '\r':
            continue
        if ch < ' ' or ch > '~':
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
        if has_invalid_ascii(deciphered.get_ascii()):
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
