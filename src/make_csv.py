#!/usr/bin/env python3

import argparse
import sys 
from os.path import exists
#import glob 

if len(sys.argv) > 1:
    txtname = sys.argv[1]
    print(txtname)
    print('This first arg should be the blob name for the GPT engine files.')

parser = argparse.ArgumentParser(description='Make csv file from the movie corpus file using gpt engines.')
#parser.add_argument('--model_list', metavar='MODEL', default="gpt2,gpt2-medium,gpt2-large,gpt2-xl,gptj-pipeline,gpt3-curie,gpt3" ,type=str, help='Code word GPT model list. Series of several strings ("gpt2", "gptj", "gpt3").')
parser.add_argument("--tabname", default="tabname.csv", type=str, help="Output csv file name.")
#parser.add_argument('--length', default=1000, type=int, help="Length, in sentences, of output file.")
parser.add_argument("--screen", action="store_true", help="Print verbose output to screen.")
#parser.add_argument("--num_repeats", default=-1, type=int, help="Number of repeats to report on-screen.")
args = parser.parse_args()

if __name__ == "__main__":
    x = []
    y = []
    z = []
    data_name = "../data/" + args.tabname.split(".")[0] + ".maker.tsv"
    if exists(data_name):
        files = open(data_name ,"r")
        for i in files:
            ii = i.split("\t")
            ii = [x.strip() for x in ii]
            x.append(ii)
        files.close()
    details_name = "../csv/details.csv"
    if exists(details_name):
        files = open(details_name, "r")
        for i in files:
            ii = i.split(",")
            ii = [x.strip() for x in ii]
            y.append(ii)
        files.close()
    for i in y:
        for j in x:
            if i[0] == j[-2]:
                ii = i + [j[3], j[5], j[7]]
                print(ii)
                z.append(ii)
        #print(i)
    pass 
