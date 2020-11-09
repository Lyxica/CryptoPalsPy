from SingleCharXor import scan_and_sort, chi_sort
from TextView import from_ascii, from_hexstr, TextView, chunks


def singlebyte_xor_scan_file_cipher_list(inputf, outputf):
    file = open(inputf, 'r')
    ciphers = map(lambda x: x.strip(), file.readlines())

    o = []
    for ciph in ciphers:
        tv = from_hexstr(ciph)
        results = scan_and_sort(tv)
        if len(results) == 0:
            continue
        o.append(results[0])
    o = chi_sort(o)

    with open(outputf, 'w', encoding='utf8') as f:
        for view in o:
            f.write("{0}\n-------------------------------\n".format(view[0].get_ascii()))