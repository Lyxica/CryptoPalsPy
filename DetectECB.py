from typing import Optional
import itertools
import Utils


def _find_repeat_blocks(block_size: int, data: bytes) -> Optional[tuple[int, bytes]]:
    chunked_blocks = Utils.chunks(data, block_size // 8)

    for k, g in itertools.groupby(sorted(chunked_blocks)):
        if len(list(g)) > 1:
            return block_size, data

    return None


def detect_ecb(cipher: bytes) -> Optional[tuple[int, bytes]]:
    for block_size in [128, 192, 256]:
        results = _find_repeat_blocks(block_size, cipher)
        if results is not None:
            return results
    return None




