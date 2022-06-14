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
    num = 0
    x = []
    y = []
    list_input = open("../data/" + file_name_in, "r")
    for l in list_input:
        line = l.split("\t")
        x.append(line)
        y.append(1)
        num += 1 
        if num >= args.length: break 
        
    list_input.close()
    if args.screen: print("len of input in lines", len(x))
    for j in range(len(x)):
        if args.screen: print("working on line index", j)
        for k in range(j+1, len(x)):
            if args.screen: print("compare line index", k)
            if y[j] != 0 and x[j][1].strip() == x[k][1].strip():
                y[j] += 1 
                y[k] = 0

    z = args.length
    tot = 0
    num = 0
    file_name_out = args.tabname.split(".")[0] + "." + args.model + ".compare.tsv"
    list_output = open("../data/" + file_name_out, "w")
    for m in range(len(x)):
        if args.screen: print(y[m])
        if y[m] > 1:
            list_output.write(str(m) + "\t" + x[m][0].strip() + "\t" + x[m][1].strip() + "\t" + str(y[m]) + "\n")
            tot += y[m]
            num += 1 
    list_output.close()
    print ("total =", str(tot) + "/" + str(z), "num =", str(num))
    file_name_out_maker = args.tabname.split(".")[0] +  ".maker.tsv"
    maker_output = open("../data/" + file_name_out_maker, "a")
    maker_output.write("making " + file_name_out + " = " + str(tot) + "/" + str(z) + "\t" + str(tot) + "\t" + str(z) + "\t" + str(num) + "\t" + args.model + "\n")
