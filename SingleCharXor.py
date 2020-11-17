from __future__ import annotations
from typing import NewType
from TextView import TextView, from_ascii, from_hexstr
from Histogram import Histogram
import time

HexStr = NewType('HexStr', str)
Key = NewType('Key', str)
Plaintext = NewType('Plaintext', str)


def has_invalid_ascii(input: str) -> bool:
    return False
    print(input)
    for ch in input:
        if ch == '\n':
            continue
        if ch == '\r':
            continue
        if ch < ' ' or ch > '~':
            return True
    return False


def xor_scan(data: TextView) -> list[tuple[TextView, int]]:
    byte_len = len(data)
    raw_xors = []
    for i in range(256):
        # ih = hex(i)[2:]
        # key = "{0:02x}".format(i)
        deciphered = otp_xor(data, TextView(bytes([i] * byte_len)))
        # if i == 118:
        #     print(deciphered.get_ascii())
        if has_invalid_ascii(deciphered.get_ascii()):
            continue

        raw_xors.append((deciphered, i))

    return raw_xors


def otp_xor(data: TextView, key: TextView) -> TextView:
    return data ^ key


def scan_and_sort(target: TextView, len: int = 5):
    items = xor_scan(target)
    histogram = Histogram(mode="ENGLISH")
    scored_items = sorted(items, key=lambda x: histogram.score(x[0].get_bytes()))
    return scored_items[:len]

if __name__ == '__main__':
    target = from_hexstr('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')
    o = scan_and_sort(target)
    for item in o:
        data, key = item
        o = data.get_ascii()
        print("".join(o) + " -> " + chr(key))
