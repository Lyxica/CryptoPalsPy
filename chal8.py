import TextView
from typing import Union, Literal
import Histogram
import SingleCharXor
from functools import partial, reduce
import binascii
import itertools


def find_repeat_blocks(block_size: int, data: bytes) -> Union[None, tuple[int, bytes]]:
    chunked_blocks = TextView.chunks(data, block_size // 8)

    for k, g in itertools.groupby(sorted(chunked_blocks)):
        if len(list(g)) > 1:
            return block_size, data

    return None


def detect_ecb_in_cipher(cipher: bytes) -> Union[None, tuple[Union[Literal[128], Literal[192], Literal[256], bytes]]]:
    for block_size in [128, 192, 256]:
        results = find_repeat_blocks(block_size, cipher)
        if results is not None:
            return results
    return None




