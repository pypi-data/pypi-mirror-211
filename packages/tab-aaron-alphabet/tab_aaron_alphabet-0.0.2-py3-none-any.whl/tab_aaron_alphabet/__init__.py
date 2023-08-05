import argparse as _argparse

import os_aaron_alphabet as _os

parser = _argparse.ArgumentParser(
    fromfile_prefix_chars='@',
    allow_abbrev=False,
)
parser.add_argument('targets', nargs='*')

def main(args=None):
    ns = parser.parse_args(args)
    if len(ns.targets):
        targets = ns.targets
    else:
        targets = ['.']
    files = _os.walk(*targets)
    for file in targets:
        if _os.os.path.splitext(file)[1] != ".py":
            continue
        with open(file, 'r') as s:
            text = s.read()
        text = text.replace('\t', "    ")
        with open(file, 'w') as s:
            s.write(text) 
