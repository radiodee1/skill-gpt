#!/usr/bin/env python3

import argparse
import sys

if len(sys.argv) > 1:
    txtname = sys.argv[1]
    print(txtname)
    print('This first arg should be the path to the movie corpus file.')

parser = argparse.ArgumentParser(description='Make tab file from the movie corpus file.')
parser.add_argument('basefile', metavar='FILE', type=str, help='Base file from movie corpus for tab output.')
parser.add_argument("--tabname", default="tabname.tsv", type=str, help="Resulting tab file name.")
parser.add_argument('--length', default=1000, type=int, help="Length, in sentences, of output file.")
parser.add_argument("--do_format", action="store_true", help="Format or not format.")
args = parser.parse_args()


