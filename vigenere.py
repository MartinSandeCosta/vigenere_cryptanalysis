import argparse
import sys
import hashlib
from math import ceil
from functools import reduce as funcreduce
from operator import iconcat
from itertools import product


MOST_COMMON_LETTER = ('E', 4)

WORD_LENGTH = 4
KEY_LENGTH_THRESHOLD = 4
OCCURRENCES_THRESHOLD = 5


def decipher(string, key, a2i_dict, i2a_dict):
    """
    This function is BASED on https://github.com/jameslyons/pycipher
    """
    key = [k.upper() for k in key]
    ret = ''
    for (i, c) in enumerate(string):
        i = i % len(key)
        ret += i2a_dict[(a2i_dict[c] - a2i_dict[key[i]]) % len(a2i_dict)]
    return ret


def count_word_occurrences(text, length):
    word_occurrences = {}
    max_occurrences = 0
    for i in range(len(text)-length):
        word = text[i:i+length]
        if word in word_occurrences:
            word_occurrences[word][0] += 1
            word_occurrences[word][1].append(i)
        else:
            word_occurrences.update({word: [1, [i]]})
        max_occurrences = max(word_occurrences[word][0], max_occurrences)

    occurrences_threshold = ceil(max_occurrences*0.66)

    return {word: list(map(lambda x, y: y-x, indexes[:-1], indexes[1:]))
            for (word, [occurrences, indexes]) in word_occurrences.items()
            if occurrences >= occurrences_threshold}


def get_divs(_int):
    yield _int
    for i in range(2, int(_int / 2) + 1):
        mod = _int % i
        if mod == 0:
            yield i


def key_lengths(int_list):
    occurrences = {}
    for _int in int_list:
        divs = list(get_divs(_int))
        for div in divs:
            if div in occurrences:
                occurrences[div] += 1
            else:
                occurrences.update({div: 1})

    return [key
            for key, ocurrence in reversed(sorted(occurrences.items(), key=lambda item: item[1]))
            if ocurrence != 1
            ] + [1]


def find_occurrences(key_length, input_text, occurences_threshold):
    occurrences_trimmed = []
    for index in range(key_length):
        occurrences = {}
        for checked in range(0, len(input_text)-key_length, key_length):
            letter = input_text[index+checked]
            if letter in occurrences:
                occurrences[letter] += 1
            else:
                occurrences.update({letter: 1})
        occurrences = sorted(occurrences.items(),
                             key=lambda item: item[1], reverse=True)
        occurrences_trimmed.append([letter
                                    for letter, _frequency in occurrences[0:occurences_threshold]
                                    ])
    return occurrences_trimmed


def main():
    argparser = argparse.ArgumentParser(prog='vigenere')
    argparser.add_argument('-i', '--input', type=argparse.FileType(), help='input file')
    argparser.add_argument('-d', '--dictionary', type=argparse.FileType(),
                           help='file with the dictionary to be used')
    argparser.add_argument('--hash', type=argparse.FileType(),
                           help='file with the hash to be used for comparison')
    argparser.add_argument('-wl', '--word-length', type=int,
                           help='length of words for ocurrence count in length guessing (Kasiski)' +
                           f': defaults to {WORD_LENGTH}')
    argparser.add_argument('-klt', '--key-length-threshold', type=int,
                           help='number of key length candidates to examine (Kasiski)' +
                           f': defaults to {KEY_LENGTH_THRESHOLD}')
    argparser.add_argument('-ot', '--occurrences-threshold', type=int,
                           help=f'number of top letters to examine for each column (Kasiski)'+
                           f': defaults to {OCCURRENCES_THRESHOLD}')
    argparser.add_argument('-v', '--verbose', action='store_true', help='enables verbose mode')
    args = argparser.parse_args()

    if (not args.input) or (not args.dictionary) or (not args.hash):
        sys.exit(argparser.print_help())

    # Kasiski arguments
    word_length = args.word_length if args.word_length else WORD_LENGTH
    key_length_threshold = args.key_length_threshold if args.key_length_threshold else KEY_LENGTH_THRESHOLD
    occurrences_threshold = args.occurrences_threshold if args.occurrences_threshold else OCCURRENCES_THRESHOLD

    # Dictionaries generation
    a2i_dict, i2a_dict = {}, {}
    for (index, value) in enumerate(args.dictionary.read().replace('\n', '')):
        a2i_dict.update({value: index})
        i2a_dict.update({index: value})

    if args.verbose:
        print(f'DEBUG\tDictionary: {a2i_dict.keys()}')

    # Input text preprocessing
    input_text = args.input.read().replace('\n', '')

    # Hash preprocessing
    input_hash = args.hash.read().replace('\n', '')

    # Propose key lengths
    most_ocurrent_words = count_word_occurrences(
        input_text, word_length)
    key_length_candidates = key_lengths(
        set(funcreduce(iconcat, most_ocurrent_words.values(), [])))
    if args.verbose:
        print(f'DEBUG\tKey length candidates: {key_length_candidates}')

    # Decipher
    for key_length in key_length_candidates[0:key_length_threshold]:
        if args.verbose:
            print(f'DEBUG\tTrying keylength: {key_length}')

        occurrences = find_occurrences(key_length, input_text, occurrences_threshold)

        letter_key_candidates = []
        for letters in occurrences:
            common_column_letters = []
            for letter in letters:
                common_column_letters.append(i2a_dict[
                    (a2i_dict[letter]-MOST_COMMON_LETTER[1]) % len(a2i_dict)
                ])
            letter_key_candidates.append(common_column_letters)

        for key_candidate in product(*letter_key_candidates):
            decrypted_text = decipher(
                input_text, key_candidate, a2i_dict, i2a_dict)
            if hashlib.sha256(decrypted_text.encode('utf-8')).hexdigest() == input_hash:
                print(f'{"".join(key_candidate)}')
                sys.exit()

    sys.exit('A key has not be found under the following Kasiski configuration:\n' + \
             f'\t--word-length={word_length}\n' + \
             f'\t--key-length-threshold={key_length_threshold}\n' + \
             f'\t--occurrences-threshold={occurrences_threshold}\n' + \
             'These heuristics are too restrictive. Try again changing the configuration values!')


if __name__ == "__main__":
    main()
