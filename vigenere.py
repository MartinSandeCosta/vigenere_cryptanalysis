import argparse
import sys
import re
import hashlib

HELP = """
usage: vigenere [-h] [-i INPUT] [-d DICTIONARY] [--hash HASH]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input file
  -d DICTIONARY, --dictionary DICTIONARY
                        file with the dictionary to be used
  --hash HASH           file with the hash to be used for comparison
"""


def decipher(string, key, a2i_dict, i2a_dict):
    """
    Based on https://github.com/jameslyons/pycipher
    """
    key = [k.upper() for k in key]
    ret = ''
    for (i, c) in enumerate(string):
        i = i % len(key)
        ret += i2a_dict[(a2i_dict[c] - a2i_dict[key[i]]) % len(a2i_dict)]
    return ret


def main():
    argparser = argparse.ArgumentParser(prog='vigenere')
    argparser.add_argument('-i', '--input', type=argparse.FileType(), help='input file')
    argparser.add_argument('-d', '--dictionary', type=argparse.FileType(), help='file with the dictionary to be used')
    argparser.add_argument('--hash', type=argparse.FileType(), help='file with the hash to be used for comparison')
    args = argparser.parse_args()

    if (not args.input) or (not args.dictionary) or (not args.hash):
        sys.exit(HELP)

    # Dictionaries generation
    a2i_dict, i2a_dict = {}, {}
    for (index, value) in enumerate(args.dictionary.read().replace('\n', '')):
        a2i_dict.update({value: index})
        i2a_dict.update({index: value})

    # Input text preprocessing
    input_text = re.sub('[^A-Z]', '', args.input.read().upper())

    # Hash preprocessing
    input_hash = args.hash.read().replace('\n', '')

    # Decrypted text
    print(decipher(input_text, 'LUZ', a2i_dict, i2a_dict))


if __name__ == "__main__":
    main()
