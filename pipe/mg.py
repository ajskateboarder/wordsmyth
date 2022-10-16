#!/usr/bin/env python3

import sys
import ast

inputs = list(sys.stdin)
for i in inputs:
    print(ast.literal_eval(i.strip()))
