import Crypto.Cipher.AES as AES
import base64


x = AES.new(key="YELLOW SUBMARINE".encode("utf8"), mode=AES.MODE_ECB)
with open('ChallengeFiles/7.txt', 'rb') as f:
    base_data = base64.b64decode(f.read())
    data = x.decrypt(base_data)
    print("".join(map(chr, data)))
