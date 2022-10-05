#!/usr/bin/python

from ast import literal_eval
import sys

print(literal_eval(list(sys.stdin)[-1]))
