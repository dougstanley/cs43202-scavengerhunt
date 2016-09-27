#!/bin/bash

ARG=$1
USER=$(echo $ARG|cut -d'/' -f1)
URL="https://web.cs.kent.edu/~"${ARG}".tar.gz"
FILE=${USER}".tar.gz"

# Fetch file
curl -s -k -o $FILE "$URL" || echo "Download failed!"

if [ -f "$FILE" ]; then
    ./auto_grade.py $FILE || echo "Grading failed!"
else
    echo "File to check not found, download probably failed!"
    exit 1
fi

# check they created the file
ssh wasp.cs.kent.edu 'ls -l hunt/students/'${USER}
