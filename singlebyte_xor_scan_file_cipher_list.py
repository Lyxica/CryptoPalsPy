from SingleCharXor import scan_and_sort
from Histogram import Histogram
from CipherText import from_ascii, from_hexstr, CipherText
import time
from typing import Iterable, Sequence

import multiprocessing


def f(x):
    return scan_and_sort(from_hexstr(x))


def extract_bytes(item: tuple[CipherText, int]) -> bytes:
    return item[0].get_bytes()


def singlebyte_xor_scan_file_cipher_list(inputf, len: int = 5) -> Sequence:
    with open(inputf, 'r') as file:
        ciphers = map(lambda x: x.strip(), file.readlines())

    with multiprocessing.Pool() as pool:
        o = pool.map(f , ciphers)

    flattened = []
    for sub_list in o:
        flattened.extend(sub_list)

    histogram = Histogram()
    sorted_items = sorted(flattened, key=lambda x: histogram.score(x[0].get_bytes()))

    return sorted_items[:len]