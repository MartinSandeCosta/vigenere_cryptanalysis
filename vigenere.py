import argparse
import sys
import re
import hashlib
from math import ceil, gcd
from functools import reduce as funcreduce
from operator import iconcat


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


def count_word_ocurrences(text, length):
    word_ocurrences = {}
    max_ocurrences = 0
    for i in range(len(text)-length):
        word = text[i:i+length]
        if word in word_ocurrences:
            word_ocurrences[word][0] += 1
            word_ocurrences[word][1].append(i)
        else:
            word_ocurrences.update({word: [1, [i]]})
        if word_ocurrences[word][0] > max_ocurrences:
            max_ocurrences = word_ocurrences[word][0]

    ocurrences_threshold = ceil(max_ocurrences*0.66)

    return {word: list(map(lambda x, y: y-x, indexes[:-1], indexes[1:]))
            for (word, [ocurrences, indexes]) in word_ocurrences.items()
            if ocurrences >= ocurrences_threshold}


def list_gcd(int_list):
    return funcreduce(lambda x, y: gcd(x, y), int_list)


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

    most_ocurrent_words = count_word_ocurrences(input_text, 4)
    key_length = list_gcd(set(funcreduce(iconcat, most_ocurrent_words.values(), [])))
    print(f'Key length: {key_length}')

    # Key generation
    key = 'luz'

    # Decrypted text
    decrypted_text = decipher(input_text, key, a2i_dict, i2a_dict)

    # Key test
    test = hashlib.sha256(decrypted_text.encode('utf-8')).hexdigest() == input_hash

    print(f'Key: {key}, Test: {test}')


if __name__ == "__main__":
    main()
