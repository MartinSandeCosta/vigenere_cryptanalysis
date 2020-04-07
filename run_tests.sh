#!/bin/bash

JDP_LENGTH=4
VERBOSE=''

while getopts v opt; do
    case "$opt" in
    v)
        VERBOSE='-v'
        ;;
    \?)
       echo "Option '-$OPTARG' is not a valid option." >&2
       instructions
       exit 1
       ;;
    esac
done

for i in $(seq -f "%03g" 001 ${JDP_LENGTH})
do
    echo "Solving: Jdp_${i}"
    python3 vigenere.py -i test/JdP_${i}_input -d test/JdP_${i}_dictionary --hash test/JdP_${i}_hash ${VERBOSE}
    echo ""
done