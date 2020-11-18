import CipherText
import base64
from typing import TypeVar
from collections.abc import Callable, Sequence, Sized
import SingleCharXor
from itertools import islice
from operator import eq
from functools import partial
import multiprocessing
import Utils


def _hamming_distance(a: bytes, b: bytes) -> int:
    assert(len(a) == len(b))

    def int2binstr(char: int):
        return "{0:08b}".format(char)

    a_prime = "".join(map(int2binstr, a))
    b_prime = "".join(map(int2binstr, b))
    zipped = zip(a_prime, b_prime)

    return len(list(filter(lambda x: x[0] != x[1], zipped)))


def _find_keylen(cipher: bytes, max_key_len: int = 40, result_count: int = 100) -> list[tuple[int, float]]:
    def same_size(a: Sized, b: Sized):
        return len(a) == len(b)

    distances = []
    for key_len in range(2, max_key_len):
        blocks = Utils.chunks(cipher, key_len)
        filtered_blocks = filter(partial(same_size, blocks[0]), blocks)

        dist = Utils.slide(list(filtered_blocks)[:50], _hamming_distance) / key_len
        distances.append((key_len, dist))

    return distances[:result_count]


def __get_key_ch(data: bytes) -> int:
    tv = CipherText.CipherText(data)
    results = SingleCharXor.recover_plaintext(tv)
    return results[0][1]


def recover_key(data: bytes):
    distances = _find_keylen(data)
    likely_keylen = sorted(distances, key=lambda x: x[1])[0][0]
    blocks = Utils.chunks(data, likely_keylen)
    transposed = {}

    for block in blocks:
        for i, b in enumerate(block):
            try:
                transposed[i].append(b)
            except KeyError:
                transposed[i] = [b]

    list_of_transposed_blocks = []
    for key in transposed.keys():
        list_of_transposed_blocks.append(transposed[key])

    with multiprocessing.Pool() as pool:
        key_chars = pool.map(__get_key_ch, list_of_transposed_blocks)
        return "".join(map(chr, key_chars))
