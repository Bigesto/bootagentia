import os
import sys
import string

print(sys.argv)

for arg in sys.argv[::-1]:
    if arg.startswith("--"):
        print(arg)