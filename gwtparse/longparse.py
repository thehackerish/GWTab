#!/usr/local/bin/python

import sys
import math
import string

if len(sys.argv) < 3:
    print "%s <mode> <code>" % sys.argv[0]
    sys.exit(-1)

value   = sys.argv[2]
rfc4648 = list(string.ascii_uppercase + string.ascii_lowercase + string.digits)

def decode(code):
    num = 0
    i = len(code)-1

    for c in code:
        num += int(rfc4648.index(c)*math.pow(64, i))
        i -= 1
    return int(num)


def encode(number):
    number = int(number)
    r = []
    out = ""
    while number>0:
        r.append(number%64)
        number = number/64
    for i in r:
        out += rfc4648[i]
    return out[::-1]

if sys.argv[1] == "d":
    print decode(value)
else:
    print encode(value) 

