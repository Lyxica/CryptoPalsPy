def gen_histogram(input: str):
    input = input.lower()
    total_len = len(input)
    o = {}
    for key in eng_historgram().keys():
        sub_len = len(list(filter(lambda x: x == key, input)))
        o[key] = sub_len / total_len

    return o

def eng_historgram():
    histogram = {}
    for i in range(256):
        histogram[chr(i)] = 0.0000000000000000001

    histogram['e'] = 0.111607
    histogram['m'] = 0.030129
    histogram['a'] = 0.084966
    histogram['h'] = 0.030034
    histogram['r'] = 0.075809
    histogram['g'] = 0.024705
    histogram['i'] = 0.075448
    histogram['b'] = 0.020720
    histogram['o'] = 0.071635
    histogram['f'] = 0.018121
    histogram['t'] = 0.069509
    histogram['y'] = 0.017779
    histogram['n'] = 0.066544
    histogram['w'] = 0.012899
    histogram['s'] = 0.057351
    histogram['k'] = 0.011016
    histogram['l'] = 0.054893
    histogram['v'] = 0.010074
    histogram['c'] = 0.045388
    histogram['x'] = 0.002902
    histogram['u'] = 0.036308
    histogram['z'] = 0.002722
    histogram['d'] = 0.033844
    histogram['j'] = 0.001965
    histogram['p'] = 0.031671
    histogram['q'] = 0.001962
    histogram[' '] = 0.171662

    return histogram
