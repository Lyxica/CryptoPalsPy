import TextView



def encryptdecrypt(pt, key) -> TextView:
    output = []
    key_len = len(key)
    for i, ch in enumerate(pt):
        output.append(ord(key[i % key_len]) ^ ord(ch))
    return TextView.from_ascii("".join(map(chr, output)))

if __name__ == "__main__":
    pt = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    key = "ICE"
    e = encryptdecrypt(pt, key)
    print(e.get_hexstr())
