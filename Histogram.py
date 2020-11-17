import CipherText
from typing import Iterable, TypeVar, Sequence
import time
import functools


class Histogram:
    base = {}

    def __init__(self, mode="ENGLISH"):
        if mode == "ENGLISH":
            self.__set_english()
        elif mode == "RANDOM":
            self.__set_random()
        else:
            raise TypeError

    def __set_random(self):
        histogram = {}
        for i in range(256):
            histogram[i] = 1 / 256
        self.base = histogram

    def __set_english(self):
        histogram = {}
        for i in range(256):
            histogram[i] = 0.0000000000000000001

        histogram[ord('e')], histogram[ord('E')] = [0.111607, 0.111607]
        histogram[ord('m')], histogram[ord('M')] = [0.030129, 0.030129]
        histogram[ord('a')], histogram[ord('A')] = [0.084966, 0.084966]
        histogram[ord('h')], histogram[ord('H')] = [0.030034, 0.030034]
        histogram[ord('r')], histogram[ord('R')] = [0.075809, 0.075809]
        histogram[ord('g')], histogram[ord('G')] = [0.024705, 0.024705]
        histogram[ord('i')], histogram[ord('I')] = [0.075448, 0.075448]
        histogram[ord('b')], histogram[ord('B')] = [0.020720, 0.020720]
        histogram[ord('o')], histogram[ord('O')] = [0.071635, 0.071635]
        histogram[ord('f')], histogram[ord('F')] = [0.018121, 0.018121]
        histogram[ord('t')], histogram[ord('T')] = [0.069509, 0.069509]
        histogram[ord('y')], histogram[ord('Y')] = [0.017779, 0.017779]
        histogram[ord('n')], histogram[ord('N')] = [0.066544, 0.066544]
        histogram[ord('w')], histogram[ord('W')] = [0.012899, 0.012899]
        histogram[ord('s')], histogram[ord('S')] = [0.057351, 0.057351]
        histogram[ord('k')], histogram[ord('K')] = [0.011016, 0.011016]
        histogram[ord('l')], histogram[ord('L')] = [0.054893, 0.054893]
        histogram[ord('v')], histogram[ord('V')] = [0.010074, 0.010074]
        histogram[ord('c')], histogram[ord('C')] = [0.045388, 0.045388]
        histogram[ord('x')], histogram[ord('X')] = [0.002902, 0.002902]
        histogram[ord('u')], histogram[ord('U')] = [0.036308, 0.036308]
        histogram[ord('z')], histogram[ord('Z')] = [0.002722, 0.002722]
        histogram[ord('d')], histogram[ord('D')] = [0.033844, 0.033844]
        histogram[ord('j')], histogram[ord('J')] = [0.001965, 0.001965]
        histogram[ord('p')], histogram[ord('P')] = [0.031671, 0.031671]
        histogram[ord('q')], histogram[ord('Q')] = [0.001962, 0.001962]
        histogram[ord(' ')] = 0.171662

        self.base = histogram

    def __create_histogram(self, data: bytes):
        total_len = len(data)
        o = {}
        for _byte in range(256):
            sub_len = len(list(filter(lambda x: x == _byte, data)))
            o[_byte] = sub_len / total_len

        return o

    def sort(self, data: Sequence[bytes]):
        histograms = map(self.__create_histogram, data)
        scored_data = self.__score_items(histograms)
        sorted_data = sorted(scored_data, key=lambda x: x[0])

        return list(map(lambda x: x[0], sorted_data))

    def score(self, data: bytes):
        histogram = self.__create_histogram(data)
        return self.__score(histogram)

    def chi(self, w, f):
        return pow(f - w, 2) / w

    def __score(self, freqs):
        n = 0
        for key in range(256):
            n += self.chi(self.base[key], freqs[key])
        return n


    def score_items(self, data: Sequence[bytes]):
        histograms = map(self.__create_histogram, data)
        scored_data = self.__score_items(histograms)
        scores = map(lambda x: x[0], scored_data)
        scored_sequence = list(map(lambda x: (x[0], x[1]), zip(scores, data)))
        return scored_sequence

    def __score_items(self, items):
        def chi(w, f):
            return pow(f - w, 2) / w

        def score(freqs):
            n = 0
            for key in range(256):
                n += chi(self.base[key], freqs[key])
            return n

        return map(lambda x: (score(x), x), items)
