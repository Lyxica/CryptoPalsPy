import CipherText


def encryptdecrypt(pt, key) -> CipherText:
    output = []
    key_len = len(key)
    for i, ch in enumerate(pt):
        output.append(ord(key[i % key_len]) ^ ord(ch))
    return CipherText.from_ascii("".join(map(chr, output)))

if __name__ == "__main__":
    pt = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    key = "ICE"
    e = encryptdecrypt(pt, key)
    print(e.get_hexstr())
