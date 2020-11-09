from __future__ import annotations
import typing
import struct

HexStr = typing.NewType('HexStr', str)  # Looks like this: '68656c6c6f20776f726c64' -> hello world

def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))


class TextView:
    text: str

    def __init__(self, ascii_str: str):
        self.text = ascii_str

    def __len__(self):
        return len(self.text)

    def get_ascii(self) -> str:
        return self.text

    def get_hexstr(self) -> HexStr:
        return HexStr("".join(list(map(lambda x: "{0:02x}".format(ord(x)), self.text))))

    def get_bytes(self) -> bytes:
        return self.text.encode('utf8')
        return bytes(bytearray(self.text, 'utf8'))


def from_ascii(ascii: str) -> TextView:
    return TextView(ascii)


def from_hexstr(hexstr: HexStr) -> TextView:
    assert(len(hexstr) % 2 == 0)
    chars = chunks(hexstr, 2)
    int_chars = map(lambda x: int(x, 16), chars)
    ascii_str = "".join(map(lambda x: chr(x), int_chars))
    return TextView(ascii_str)


if __name__ == "__main__":
    x = TextView("Hello World")
    print(x.get_ascii())
    print(x.get_hexstr())
    n = x.get_bytes()
    print(n)
    print(hex(n[0] ^ n[1]))