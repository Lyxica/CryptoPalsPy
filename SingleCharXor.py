from __future__ import annotations
import base64
import Histogram
import binascii
import struct
from typing import NewType
import TextView
from TextView import TextView, from_ascii, from_hexstr
from functools import reduce

HexStr = NewType('HexStr', str)
Key = NewType('Key', str)
Plaintext = NewType('Plaintext', str)


def has_invalid_ascii(input: str) -> bool:
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
        ih = hex(i)[2:]
        key = "{0:02x}".format(i)
        deciphered = otp_xor(data, from_hexstr(key * byte_len))
        if has_invalid_ascii(deciphered.get_ascii()):
            continue

        raw_xors.append((deciphered, i))

    return raw_xors


def chi_sort(_items: list[tuple[TextView, int]]):
    english = Histogram.eng_historgram()

    def chi(w, f):
        return pow(f - w, 2) / w

    def score(item: tuple[TextView, int]):
        data, _ = item
        n = 0
        freqs = Histogram.gen_histogram(data.get_ascii())
        for key in english.keys():
            n += chi(english[key], freqs[key])
        return n

    return sorted(_items, key=score, reverse=False)


def otp_xor(data: TextView, key: TextView) -> TextView:
    assert(len(data) == len(key))
    n = []
    for p in zip(data.get_bytes(), key.get_bytes()):
        n.append(chr(p[0] ^ p[1]))

    return from_ascii("".join(n))


def scan_and_sort(target: TextView):
    items = xor_scan(target)
    o = []
    for tup in items:
        _bytes = tup[0].get_ascii()
        contains_bad_ascii = reduce(lambda a, b: a or (b < ' ' or b > '~'), _bytes, False)
        if not contains_bad_ascii:
            o.append(tup)
        else:
            o.append(tup)

    items = chi_sort(o)
    return items

if __name__ == '__main__':
    target = from_hexstr('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')
    o = scan_and_sort(target)
    for item in o:
        data, key = item
        o = data.get_ascii()
        print("".join(o) + " -> " + chr(key))