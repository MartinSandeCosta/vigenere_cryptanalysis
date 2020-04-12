#!/bin/bash

JDP_LENGTH=6
VERBOSE=''
TIMEFORMAT='%3R'

instructions() {
    echo """usage: run_tests.sh
optional arguments:
    -h, --help      show this help message and exit
    -v              enables verbose mode
    -t              shows elapsed time for each instance"""
}

while getopts "vh" opt; do
    case "$opt" in
    v)
        VERBOSE='-v'
        ;;
    h)
        instructions
        exit 0
        ;;
    \?)
        echo "Option '-$OPTARG' is not a valid option." >&2
        instructions
        exit 1
        ;;
    esac
done

for i in $(seq -f "%03g" 001 ${JDP_LENGTH}); do
    echo "Solving: Jdp_${i}"
    time python3 vigenere.py -i test/JdP_${i}_input -d test/JdP_${i}_dictionary --hash test/JdP_${i}_hash $VERBOSE
    echo ""
done
