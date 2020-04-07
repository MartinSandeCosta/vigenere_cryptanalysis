import argparse
import sys
import hashlib
from math import ceil
from functools import reduce as funcreduce
from operator import iconcat
from itertools import product


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

MOST_COMMON_SPANISH = [('E', 4), ('A', 0), ('O', 15)]
MOST_COMMON_FRENGLISH = [('E', 4), ('T', 19), ('S', 18), ('A', 0)]

WORD_LENGTH_THRESHOLD = 4
KEY_LENGTH_THRESHOLD = 4
OCURRENCES_THRESHOLD = 10


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


def get_divs(_int):
    yield _int
    for i in range(2, int(_int / 2) + 1):
        mod = _int % i
        if mod == 0:
            yield i


def key_lengths(int_list):
    ocurrences = {}
    for _int in int_list:
        divs = list(get_divs(_int))
        for div in divs:
            if div in ocurrences:
                ocurrences[div] += 1
            else:
                ocurrences.update({div: 1})

    return [key
            for key, ocurrence in reversed(sorted(ocurrences.items(), key=lambda item: item[1]))
            if ocurrence != 1
            ] + [1]


def main():
    argparser = argparse.ArgumentParser(prog='vigenere')
    argparser.add_argument('-i', '--input', type=argparse.FileType(), help='input file')
    argparser.add_argument('-d', '--dictionary', type=argparse.FileType(),
                           help='file with the dictionary to be used')
    argparser.add_argument('--hash', type=argparse.FileType(),
                           help='file with the hash to be used for comparison')
    argparser.add_argument('-v', '--verbose', action='store_true', help='enables verbose mode')
    args = argparser.parse_args()

    if (not args.input) or (not args.dictionary) or (not args.hash):
        sys.exit(HELP)

    # Dictionaries generation
    a2i_dict, i2a_dict = {}, {}
    for (index, value) in enumerate(args.dictionary.read().replace('\n', '')):
        a2i_dict.update({value: index})
        i2a_dict.update({index: value})

    if 'Ñ' in a2i_dict:
        language = 1
    else:
        language = 0

    if args.verbose:
        print(f'DEBUG\tDictionary: {a2i_dict.keys()}')

    # Input text preprocessing
    input_text = args.input.read().replace('\n', '')

    # Hash preprocessing
    input_hash = args.hash.read().replace('\n', '')

    # Propose key lengths
    most_ocurrent_words = count_word_ocurrences(input_text, WORD_LENGTH_THRESHOLD)
    key_length_candidates = key_lengths(set(funcreduce(iconcat, most_ocurrent_words.values(), [])))
    if args.verbose:
        print(f'DEBUG\tKey length candidates: {key_length_candidates}')

    # Decipher
    for key_length in key_length_candidates[0:KEY_LENGTH_THRESHOLD]:
        if args.verbose:
            print(f'DEBUG\tTrying keylength: {key_length}')
        checked = 0
        ocurrences_trimmed = []
        for index in range(key_length):
            ocurrences = {}
            for checked in range(0, len(input_text)-key_length, key_length):
                letter = input_text[index+checked]
                if letter in ocurrences:
                    ocurrences[letter] += 1
                else:
                    ocurrences.update({letter: 1})
            ocurrences = sorted(ocurrences.items(), key=lambda item: item[1], reverse=True)
            ocurrences_trimmed.append([letter
                                       for letter, _frequency in ocurrences[0:OCURRENCES_THRESHOLD]
                                       ])
        letter_key_candidates = []
        for letters in ocurrences_trimmed:
            common_column_letters = []
            for letter in letters:
                if language == 1:
                    common_column_letters.append(i2a_dict[
                        (a2i_dict[letter]-MOST_COMMON_SPANISH[0][1]) % len(a2i_dict)
                        ])
                else:
                    common_column_letters.append(i2a_dict[
                        (a2i_dict[letter]-MOST_COMMON_FRENGLISH[0][1]) % len(a2i_dict)
                        ])
            letter_key_candidates.append(common_column_letters)

        for key_candidate in product(*letter_key_candidates):
            decrypted_text = decipher(input_text, key_candidate, a2i_dict, i2a_dict)
            if hashlib.sha256(decrypted_text.encode('utf-8')).hexdigest() == input_hash:
                print(f'{"".join(key_candidate)}')
                sys.exit()


if __name__ == "__main__":
    main()
