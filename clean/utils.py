# coding = utf8
from __future__ import print_function
import sys
f = open("out.txt", "w")

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def fprint(*args, **kwargs):
    print(*args, file=f, **kwargs)