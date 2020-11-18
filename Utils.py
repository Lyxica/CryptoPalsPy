from collections.abc import Sequence, Callable
from typing import TypeVar, Union

T = TypeVar('T')
K = TypeVar('K')
AnySequence = Union[Sequence[Sequence[T]], Sequence[bytes]]


def chunks(l: Union[Sequence[T], bytes], n: int) -> AnySequence:
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]


def slide(items: Sequence[T], f: Callable[[T, T], K]) -> K:
    if len(items) <= 1:
        return 0

    return f(items[0], items[1]) + slide(items[1:], f)
