import argparse
import sys

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

def main():
    argparser = argparse.ArgumentParser(prog='vigenere')
    argparser.add_argument('-i', '--input', type=argparse.FileType(), help='input file')
    argparser.add_argument('-d', '--dictionary', type=argparse.FileType(), help='file with the dictionary to be used')
    argparser.add_argument('--hash', type=argparse.FileType(), help='file with the hash to be used for comparison')
    args = argparser.parse_args()

    if (not args.input) or (not args.dictionary) or (not args.hash):
        sys.exit(HELP)


if __name__ == "__main__":
    main()
