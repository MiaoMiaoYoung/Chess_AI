# coding = utf8
import sys
f = open("out.txt", "w")

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)