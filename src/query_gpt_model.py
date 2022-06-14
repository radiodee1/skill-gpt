#!/usr/bin/env python3

import argparse
import sys
from os.path import exists

#import os
import openai 
from dotenv import dotenv_values

from transformers import GPTJForCausalLM, AutoTokenizer, AutoModelForCausalLM
import torch


if len(sys.argv) > 1:
    txtname = sys.argv[1]
    print(txtname)
    print('This first arg should be the code name for the GPT engine.')

parser = argparse.ArgumentParser(description='Make tab file from the movie corpus file using gpt engines.')
parser.add_argument('model', metavar='MODEL', type=str, help='Code word for GPT model. One of several strings ("gpt2", "gptj", "gpt3").')
parser.add_argument("--tabname", default="tabname.tsv", type=str, help="Output tab file name.")
parser.add_argument('--length', default=1000, type=int, help="Length, in sentences, of output file.")
parser.add_argument("--screen", action="store_true", help="Print verbose output to screen.")
parser.add_argument("--crashes", default=5, type=int, help="Number of model crashes before skipping all model inputs.")
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
        self.file_name = args.tabname.split('.')[0] + '.' + args.model + ".query.tsv"
        self.input_line = "Hello there."
        self.url = "https://"
        self.header = {}
        self.body = {}
        self.is_online = False


    def setup(self):
        print ("setup filename " + self.file_name)

    def get_response(self):
        if self.model == "default":
            return self.input_line
        else:
            return self.model


class GPT2(DefaultGPT):
    def __init__(self):
        DefaultGPT.__init__(self)
        self.model = "gpt2"
        self.file_name = args.tabname.split('.')[0] + '.' + self.model + ".query.tsv"
        self.input_line = "Hello there."
        self.is_online = False

        self.engine = AutoModelForCausalLM.from_pretrained("gpt2")
        self.tokenizer = AutoTokenizer.from_pretrained("gpt2")

    def setup(self):
        pass

    def get_response(self):
        prompt = self.input_line
        inputs = self.tokenizer(prompt, return_tensors="pt").input_ids
        #print(inputs)
        outputs = self.engine.generate(inputs, do_sample=True, temperature=0.001, max_length=10, skip_special_tokens=True )
        #print(outputs, "<--")
        gen_text = self.tokenizer.batch_decode(outputs)[0]
        #print(inputs , "<<--")
        if gen_text.startswith(prompt):
            gen_text = gen_text[len(prompt):]
        gen_text = gen_text.strip()
        return gen_text
        

class GPTJ(DefaultGPT):
    def __init__(self):
        DefaultGPT.__init__(self)
        self.model = "gptj"
        self.file_name = args.tabname.split('.')[0] + '.' + self.model + ".query.tsv"
        self.input_line = "Hello there."
        self.is_online = False

        self.engine = GPTJForCausalLM.from_pretrained("EleutherAI/gpt-j-6B", revision="float16", torch_dtype=torch.float16, low_cpu_mem_usage=True)
        self.tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")

    def setup(self):
        pass 

    def get_response(self):
        prompt = self.input_line
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids
        gen_tokens = self.engine.generate(input_ids, do_sample=True, temperature=0.001, max_length=10,)
        gen_text = self.tokenizer.batch_decode(gen_tokens)[0]
         #print(inputs , "<<--")
        if gen_text.startswith(prompt):
            gen_text = gen_text[len(prompt):]
        gen_text = gen_text.strip()
        return gen_text
        


class GPT3(DefaultGPT):
    def __init__(self):
        DefaultGPT.__init__(self)
        self.model = "gpt3"
        self.file_name = args.tabname.split('.')[0] + '.' + self.model + ".query.tsv"
        self.input_line = "Hello there."
        self.is_online = True

        self.config = dotenv_values("../.env")
        print(self.config)
        openai.api_key = self.config["OPENAI_API_KEY"]
        #self.organization = self.config["OPENAI_ORGANIZATION"]

    def setup(self):
        pass

    def get_response(self):
        gen_text = openai.Completion.create(
            model="text-davinci-002",
            prompt=self.input_line,
            max_tokens=5,
            temperature=0.001
        )
        #print(gen_text , "<---")
        gen_text = gen_text["choices"][0]["text"].replace("\n","").strip()
        return gen_text
        

if __name__ == "__main__":
    skip = False
    gpt = DefaultGPT()

    if args.model == "gpt2":
        print("gpt2 model")
        try:
            gpt = GPT2()
        except:
            skip = True
    elif args.model == "gptj":
        print("gptj model")
        try:
            gpt = GPTJ()
        except:
            skip = True
    elif args.model == "gpt3":
        print("gpt3 model")
        try:
            gpt = GPT3()
        except:
            skip = True

    gpt.setup()

    print(gpt.model)
    print(gpt.file_name)
    
    if not exists("../data/" + gpt.file_name):
        save = open("../data/" + gpt.file_name, "w")
        file = open("../data/" + args.tabname, "r")
        j = []
        num = 0
        for l in file:
            if args.screen: print (l.strip())
            j.append(l.split("\t")[0])
            if args.screen: print(j[num])
            save.write(j[num] + "\t" + "\t" +  "\n")
            num += 1 
            if num >= args.length: break
        save.close()
        file.close()

    
    if exists("../data/" + gpt.file_name):
        saved = open("../data/" + gpt.file_name, 'r')
        x = []
        num = 0
        crash_count = 0 
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
                    except  KeyboardInterrupt:
                        l[1] = ""
                        skip = True
                    except:
                        l[1] = ""
                        if not gpt.is_online: skip = True
                        crash_count += 1 
                        if crash_count >= args.crashes: 
                            skip = True
                else:
                    l[1] = ""
                
                if args.screen: print(l[0], ">>" , l[1])
            x.append([ l[0], l[1] ])
            num += 1 
            if num >= args.length: break

        resave = open("../data/" + gpt.file_name, "w")
        for l in x:
            resave.write(l[0].strip() + "\t" + l[1].strip() + "\n")
        resave.close()