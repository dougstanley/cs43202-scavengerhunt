#!/bin/bash
###############################
# sticks some random generated
# text into the file specified
###############################

if [ "$#" -ne 1 ]; then
    echo "You need to specify a file to write to as one and only argument!"
    echo "$0 FILENAME"
    exit 1
fi
FILE=$1

if [ ! -e $FILE ] || [ -s $FILE ]; then
    #Lets only write to empty files that exist just to be safe
    echo "File does not exist, or is not empty, are you sure you want to"
    echo "create or overwrite $FILE?"
    exit 1
fi

NBLOCKS=$((($RANDOM%4)+1))
BSIZE=512

#flip coin and choose a hash alg to use on random bytes
#that way the file sizes vary a bit
if [ "$(($RANDOM%8))" -lt 4 ]; then
    ALG=md5sum
else
    ALG=sha1sum
fi

dd if=/dev/urandom bs=$BSIZE count=$NBLOCKS 2>/dev/null | $ALG -b | awk '{print $1}' > $FILE
