#!/bin/bash
######################################
# Take a wordlist/dictionary and
# randomly sort it and weed out
# words not suitable for directory
# or file names
#
######################################

function print_usage {
    echo "Usage:"
    echo "$0 WORDLIST"
    echo "Where:"
    echo "WORDLIST  - A sample wordlist/dictionary like"
    echo "            /usr/share/dict/words"
}

if [ "$#" -ne 1 ]; then
    print_usage
    exit 1
fi
WORDLIST=$1

if [ -f $WORDLIST ]; then
    # grab only words 3-9 characters in length, sort randomly
    grep -P -e '^[a-z]{3,9}$' $WORDLIST |sort -R
fi
