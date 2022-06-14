#!/usr/bin/env python3

import argparse
import sys 

if len(sys.argv) > 1:
    txtname = sys.argv[1]
    print(txtname)
    print('This first arg should be the code name for the GPT engine.')

parser = argparse.ArgumentParser(description='Make tab file from the movie corpus file using gpt engines.')
parser.add_argument('model', metavar='MODEL', type=str, help='Code word for GPT model. One of several strings ("gpt2", "gptj", "gpt3").')
parser.add_argument("--tabname", default="tabname.tsv", type=str, help="Output tab file name.")
parser.add_argument('--length', default=1000, type=int, help="Length, in sentences, of output file.")
parser.add_argument("--screen", action="store_true", help="Print verbose output to screen.")
args = parser.parse_args()

if __name__ == "__main__":
    file_name_in =  args.tabname.split('.')[0] + '.' + args.model + ".query.tsv"
    list_input = open("../data/" + file_name_in, "r")
    for l in list_input:
        pass 
    pass
