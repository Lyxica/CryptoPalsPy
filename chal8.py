import CipherText
from typing import Union, Literal, Optional
import Histogram
import SingleCharXor
from functools import partial, reduce
import binascii
import itertools
import Utils


def find_repeat_blocks(block_size: int, data: bytes) -> Optional[tuple[int, bytes]]:
    chunked_blocks = Utils.chunks(data, block_size // 8)

    for k, g in itertools.groupby(sorted(chunked_blocks)):
        if len(list(g)) > 1:
            return block_size, data

    return None


def detect_ecb_in_cipher(cipher: bytes) -> Optional[tuple[int, bytes]]:
    for block_size in [128, 192, 256]:
        results = find_repeat_blocks(block_size, cipher)
        if results is not None:
            return results
    return None




