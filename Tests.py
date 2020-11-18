import unittest
import CipherText
import SingleCharXor
import singlebyte_xor_scan_file_cipher_list
import chal6
import chal8
import base64
import binascii
from Utils import compose


class ChallengeTests(unittest.TestCase):

    # Implementation tests
    def test_xor(self):
        a = CipherText.from_hexstr('1234')
        b = CipherText.from_hexstr('1234')
        c = CipherText.from_hexstr('0000')

        self.assertEqual(a ^ b, '0000')
        self.assertEqual(a ^ b, c)

    # Challenge tests
    def test_challenge2(self):
        a = CipherText.from_hexstr('1c0111001f010100061a024b53535009181c')
        b = CipherText.from_hexstr('686974207468652062756c6c277320657965')

        self.assertEqual(a ^ b, '746865206b696420646f6e277420706c6179', )

    def test_challenge3(self):
        a = CipherText.from_hexstr("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")
        results = SingleCharXor.scan_and_sort(a)

        self.assertEqual(results[0][0].get_ascii(), "Cooking MC's like a pound of bacon")

    def test_challenge4(self):
        items = singlebyte_xor_scan_file_cipher_list.singlebyte_xor_scan_file_cipher_list('ChallengeFiles/4.txt')
        results = map(lambda x: x[0].get_ascii(), items)
        self.assertIn("Now that the party is jumping\n", list(results))

    def test_challenge5(self):
        a = CipherText.from_ascii("Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal")
        b = CipherText.from_ascii("ICE")

        self.assertEqual(a ^ b, "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f")

    def test_challenge6(self):
        with open('ChallengeFiles/6.txt', 'r') as data:
            decoded_data = base64.b64decode(data.read())
            x = chal6.crack_repeating_xor(decoded_data)
            self.assertEqual(x, 'Terminator X: Bring the noise')

    def test_challenge8(self):
        with open('ChallengeFiles/8.txt', 'r') as data:
            byte_lines = map(compose(binascii.unhexlify, str.strip), data.readlines())
            results = list(filter(None, map(chal8.detect_ecb_in_cipher, byte_lines)))
            self.assertEqual(len(results), 1)

            key_size, cipher = results[0]
            self.assertEqual(binascii.hexlify(cipher), b'd880619740a8a19b7840a8a31c810a3d08649af70dc06f4fd5d2d69c744cd283e2dd052f6b641dbf9d11b0348542bb5708649af70dc06f4fd5d2d69c744cd2839475c9dfdbc1d46597949d9c7e82bf5a08649af70dc06f4fd5d2d69c744cd28397a93eab8d6aecd566489154789a6b0308649af70dc06f4fd5d2d69c744cd283d403180c98c8f6db1f2a3f9c4040deb0ab51b29933f2c123c58386b06fba186a')

if __name__ == "__main__":
    unittest.main()