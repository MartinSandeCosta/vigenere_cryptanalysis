#!/bin/bash

JDP_LENGTH=4

for i in $(seq -f "%03g" 001 ${JDP_LENGTH})
do
    python3 vigenere.py -i test/JdP_${i}_input -d test/JdP_${i}_dictionary --hash test/JdP_${i}_hash
done