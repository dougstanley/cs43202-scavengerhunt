#!/usr/bin/python
#######################################
# Embed some strings in some random
# binary bytes, obfuscates text,
# but the strings command finds all
# the text.
#######################################
import sys
import struct
import random


HEADER = struct.pack(b'bbbbb', 0, 2, 1, 2, 5)
SEP = struct.pack(b'bbbb', 0, 0, 0, 0)


def usage():
    print "Usage:"
    print "%s TEXT_FILE BINARY_FILE" % sys.argv[0]
    print "Where:"
    print "TEXT_FILE    - Text file to read lines from"
    print "BINARY_FILE  - Binary file to hid text lines in."
    sys.exit(1)


def gen_bytes(n):
    """Returns n random non-printable bytes"""
    return struct.pack(n*'b', *[random.randrange(31) for i in xrange(n)])


if __name__ == '__main__':
    if len(sys.argv) != 3 or sys.argv[1] == '-h':
        usage()

    tfile = sys.argv[1]
    bfile = sys.argv[2]

    try:
        with open(tfile, 'r') as fp:
            lines = fp.readlines()
    except:
        usage()

    with open(bfile, 'wb') as fp:
        fp.write(HEADER)
        for line in lines:
            fp.write(gen_bytes(random.randrange(1024, 2048)))
            fp.write(SEP)
            fp.write(line)
            fp.write(SEP)
        fp.write(gen_bytes(random.randrange(768, 1536)))
