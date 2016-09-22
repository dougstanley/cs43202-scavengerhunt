#!/bin/bash
######################################
# Take a wordlist/dictionary and
# randomly sort it and weed out
# words not suitable for directory
# or file names
#
######################################

print_usage() {
    echo "Usage:"
    echo "$0 NUMBER RANDOMWORDS"
    echo "Where:"
    echo "NUMBER       - Number of random words to choose."
    echo "RANDOMWORDS  - Random set of words to choose from."
}

if [ "$#" -ne 2 ]; then
    print_usage
    exit 1
fi
NUM=$1
RWORDS=$2
COUNT=`wc -l $RWORDS| awk '{print $1}'`

for i in `shuf -i 1-$COUNT -n $NUM`; do
    head -n $i $RWORDS|tail -n 1
done
