#!/bin/bash

ARG=$1
USER=$(echo $ARG|cut -d'/' -f1)
URL="https://web.cs.kent.edu/~"${ARG}".tar.gz"


curl -s -k -o ${USER}".tar.gz" "$URL" || echo "Download failed!"
