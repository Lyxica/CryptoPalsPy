from typing import List, Tuple
import TextView
import base64
from functools import reduce
from funcs import *
from typing import *
import SingleCharXor


def hamming_distance(a: str, b: str) -> int:
    assert(len(a) == len(b))

    def str2bin(char: str):
        return "{0:08b}".format(ord(char))

    a_prime = "".join(map(str2bin, a))
    b_prime = "".join(map(str2bin, b))
    zipped = zip(a_prime, b_prime)

    return len(list(filter(lambda x: x[0] != x[1], zipped)))


def find_keylen(cipher: str, max_key_len: int = 40, result_count: int = 100) -> List[Tuple[int, float]]:

    def slide(items: List[str], f: Callable[[str, str], int]) -> int:
        if len(items) <= 1:
            return 0

        return f(items[0], items[1]) + slide(items[1:], f)

    distances = []
    for key_len in range(2, max_key_len):
        blocks = list(TextView.chunks(cipher, key_len))
        filtered_blocks = list(filter(lambda x: len(x) == len(blocks[0]), blocks))[:50]

        dist = slide(filtered_blocks, hamming_distance) / key_len
        distances.append((key_len, dist))

    return distances[:result_count]


if __name__ == "__main__":
    data = open('6.txt', 'r').read()
    ascii = "".join(map(chr, base64.b64decode(data)))
    distances = find_keylen(ascii)
    likely_keylen = sorted(distances, key=lambda x: x[1])[0][0]
    blocks = list(TextView.chunks(ascii, likely_keylen))
    transposed = {}

    for block in blocks[:-1]:
        for i, b in enumerate(block):
            try:
                transposed[i].append(b)
            except KeyError:
                transposed[i] = [b]
    for i, b in enumerate(blocks[-1:]):
        transposed[i].append(b)

    for key in transposed.keys():

        SingleCharXor.scan_and_sort(transposed[key])
