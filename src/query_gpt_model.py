#!/usr/bin/env python3

import argparse
import sys
from os.path import exists

from transformers import GPTJForCausalLM, AutoTokenizer
import torch


if len(sys.argv) > 1:
    txtname = sys.argv[1]
    print(txtname)
    print('This first arg should be the code name for the GPT engine.')

parser = argparse.ArgumentParser(description='Make tab file from the movie corpus file.')
parser.add_argument('model', metavar='MODEL', type=str, help='Code word for GPT model. One of several strings ("gpt2", "gptj", "gpt3").')
parser.add_argument("--tabname", default="tabname.tsv", type=str, help="Output tab file name.")
parser.add_argument('--length', default=1000, type=int, help="Length, in sentences, of output file.")
args = parser.parse_args()

class DefaultGPT:
    
    model = "default"

    file_name = "default"
    input_line = "Hello there."
    is_online = False
    url = "https://"
    header = {}
    body = {}

    def __init__(self):
        self.model = "default"
        self.file_name = "default"
        self.input_line = "Hello there."
        self.url = "https://"
        self.header = {}
        self.body = {}
        self.is_online = False


    def setup(self):
        print ("setup filename " + self.file_name)

    def make_body(self):
        print (self.body)

    def make_header(self):
        print(self.header)

    def get_response(self):
        if self.model == "default":
            return self.input_line
        else:
            return self.model

    def set_model(self, model):
        self.model = model

    def set_filename(self, filename):
        self.file_name = filename

    def set_url(self, new_url):
        self.url = new_url 

class GPT2(DefaultGPT):
    def __init__(self):
        DefaultGPT.__init__(self)
        self.model = "gpt2"
        self.file_name = args.tabname.split('.')[0] + '.' + self.model + ".query.tsv"
        self.input_line = "Hello there."
        self.url = "https://"
        self.header = {}
        self.body = {}
        self.is_online = False


class GPTJ(DefaultGPT):
    def __init__(self):
        DefaultGPT.__init__(self)
        self.model = "gptj"
        self.file_name = args.tabname.split('.')[0] + '.' + self.model + ".query.tsv"
        self.input_line = "Hello there."
        self.url = "https://"
        self.header = {}
        self.body = {}
        self.is_online = False

        self.engine = GPTJForCausalLM.from_pretrained("EleutherAI/gpt-j-6B", revision="float16", torch_dtype=torch.float16, low_cpu_mem_usage=True)
        self.tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")

    def setup(self):
        pass 

    def get_response(self):
        prompt = self.input_line
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids
        gen_tokens = self.engine.generate(input_ids, do_sample=True, temperature=0.9, max_length=100,)
        gen_text = self.tokenizer.batch_decode(gen_tokens)[0]
        return gen_text
        


class GPT3(DefaultGPT):
    def __init__(self):
        DefaultGPT.__init__(self)
        self.model = "gpt3"
        self.file_name = args.tabname.split('.')[0] + '.' + self.model + ".query.tsv"
        self.input_line = "Hello there."
        self.url = "https://"
        self.header = {}
        self.body = {}
        self.is_online = True


if __name__ == "__main__":
    gpt = DefaultGPT()

    if args.model == "gpt2":
        print("gpt2 model")
        gpt = GPT2()
    elif args.model == "gptj":
        print("gptj model")
        gpt = GPTJ()
    elif args.model == "gpt3":
        print("gpt3 model")
        gpt = GPT3()

    gpt.setup()

    print(gpt.model)
    print(gpt.file_name)

    if not exists("../data/" + gpt.file_name):
        save = open("../data/" + gpt.file_name, "w")
        file = open("../data/" + args.tabname, "r")
        j = []
        num = 0
        for l in file:
            print (l.strip())
            j.append(l.split("\t")[0])
            print(j[num])
            save.write(j[num] + "\t" + "\t" +  "\n")
            num += 1 
            if num >= args.length: break
        save.close()
        file.close()

    skip = False
    if exists("../data/" + gpt.file_name):
        saved = open("../data/" + gpt.file_name, 'r')
        x = []
        for l in saved:
            l = l.split("\t")
            if len(l) > 1 and len(l[1]) > 1:
                pass
            elif (len(l) > 1 and len(l[1]) <= 1) or len(l) == 1:
                if len(l) == 1: l.append("")
                ## replace l[1]
                if not skip:
                    try:
                        gpt.input_line = l[0]
                        l[1] = gpt.get_response()
                    except KeyboardInterrupt:
                        l[1] = ""
                        skip = True
                else:
                    l[1] = ""
                print("num" , l[1])
            x.append([ l[0], l[1] ])
        resave = open("../data/" + gpt.file_name, "w")
        for l in x:
            resave.write(l[0] + "\t" + l[1] + "\n")
        resave.close()
