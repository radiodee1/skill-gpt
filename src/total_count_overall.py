#!/usr/bin/env python3

import argparse
import sys 
from os.path import exists

if len(sys.argv) > 1:
    txtname = sys.argv[1]
    print(txtname)
    print('This first arg should be the code name for the GPT engine.')

parser = argparse.ArgumentParser(description='Make tab file from the movie corpus file using gpt engines.')
parser.add_argument('--model_list', metavar='MODEL', default="gpt2,gpt2-medium,gpt2-large,gpt2-xl,gpt3" ,type=str, help='Code word GPT model list. Series of several strings ("gpt2", "gptj", "gpt3").')
parser.add_argument("--tabname", default="tabname.tsv", type=str, help="Output tab file name.")
#parser.add_argument('--length', default=1000, type=int, help="Length, in sentences, of output file.")
parser.add_argument("--screen", action="store_true", help="Print verbose output to screen.")
parser.add_argument("--num_repeats", default=-1, type=int, help="Number of repeats to report on-screen.")
args = parser.parse_args()

if __name__ == "__main__":
    repeats = 0
    z = 0 
    file_name_out = args.tabname.split('.')[0] + "."
    if args.num_repeats > -1: repeats = args.num_repeats
    engine_record = []
    engine_visual = []
    models = args.model_list.split(",")
    for i in range(len(models)):
        #line_j = []
        ii = models[i]
        file_name_in =  args.tabname.split('.')[0] + '.' + ii + ".compare.tsv"
        if exists("../data/" + file_name_in):
            file_name_out += ii + "_"
            file = open("../data/" + file_name_in, "r")
            if args.num_repeats == -1: repeats += 1 
            for j in file:
                jj = j.split("\t")
                engine_record.append([i, jj[2].strip(), int(jj[3].strip()), 1 ])
                if args.screen: print(i, jj[2].strip(), jj[3].strip())
                pass 
            file.close()
    for k in range(len(engine_record)):
        for m in range(k + 1, len(engine_record)):
            #print(k,m)
            if engine_record[k][3] != 0 and engine_record[k][1] == engine_record[m][1]:
                engine_record[k][3] += 1 
                engine_record[m][3] = 0
                engine_record[k][2] += engine_record[m][2]
                z += 1 
                
        pass
    if args.screen: print("---")
    for k in range(len(engine_record)):
        if engine_record[k][3] >= repeats:
            engine_visual.append([ engine_record[k][3], engine_record[k][1], engine_record[k][2] ])
            print(engine_record[k][3], engine_record[k][1], engine_record[k][2])
    print(len(engine_visual))

    file_name_out += str(len(engine_visual)) + ".totals.tsv"
    print(file_name_out)
    save = open("../data/"+ file_name_out, "w")
    for n in engine_visual:
        save.write("number-of-engines:\t" + str(n[0]) + 
                "\tactual-utterance:\t" + str(n[1]) + 
                "\tnumber-of-repeats:\t" + str(n[2]) + "\n")
    save.close()
