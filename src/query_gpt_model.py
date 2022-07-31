#!/usr/bin/env python3

import argparse
import sys
from os.path import exists
import requests
import json
import os 

try:
    import openai 
except:
    pass 

from dotenv import dotenv_values
from requests.api import options

from happytransformer import HappyGeneration, GENSettings

from transformers import GPTJForCausalLM, AutoTokenizer, AutoModelForCausalLM
import torch


if len(sys.argv) > 1:
    txtname = sys.argv[1]
    print(txtname)
    print('This first arg should be the code name for the GPT engine.')
    print("examples: gpt2, gpt2-medium, gpt2-large, gpt2-xl,")
    print("    gptj, gptj-pipeline, gpt3, gpt3-babbage, gpt3-curie")
    print()

parser = argparse.ArgumentParser(description='Make tab file from the movie corpus file using gpt engines.')
parser.add_argument('model', metavar='MODEL', type=str, help='Code word for GPT model. One of several strings ("gpt2", "gptj", "gpt3").')
parser.add_argument("--tabname", default="tabname.tsv", type=str, help="Output tab file name.")
parser.add_argument('--length', default=1000, type=int, help="Length, in sentences, of output file.")
parser.add_argument("--screen", action="store_true", help="Print verbose output to screen.")
parser.add_argument("--crashes", default=5, type=int, help="Number of model crashes before skipping all model inputs.")
parser.add_argument("--huggingface", default=None, type=str, help="Huggingface model to run in place of gpt2.")
parser.add_argument("--online", action="store_true", help="Use online service for GPT Huggingface.")
parser.add_argument("--checkpoint", action="store_true", help="Use stored GPT-NEO checkpoint.")
args = parser.parse_args()


if not args.tabname.endswith(".tsv"):
    args.tabname += ".tsv"

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
    def __init__(self, model):
        DefaultGPT.__init__(self)

        self.model = model #"gpt2"
        self.file_name = args.tabname.split('.')[0] + '.' + self.model.replace("/", ".") + ".query.tsv"
        self.input_line = "Hello there."
        self.is_online = False

        self.engine = AutoModelForCausalLM.from_pretrained(self.model)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model)

    def setup(self):
        pass

    def get_response(self):
        prompt = self.input_line
        inputs = self.tokenizer(prompt, return_tensors="pt").input_ids
        
        outputs = self.engine.generate(inputs, do_sample=True, temperature=0.001, max_length=10, skip_special_tokens=True )
        
        gen_text = self.tokenizer.batch_decode(outputs)[0]
        
        if gen_text.startswith(prompt):
            gen_text = gen_text[len(prompt):]
        gen_text = gen_text.strip()
        return gen_text
        

class GPTJ(DefaultGPT):
    def __init__(self, model):
        DefaultGPT.__init__(self)
        self.model = model # "gptj"
        self.file_name = args.tabname.split('.')[0] + '.' + self.model.replace("/",".") + ".query.tsv"
        self.input_line = "Hello there."
        self.is_online = False
        self.engine = GPTJForCausalLM.from_pretrained(self.model, revision="float16", torch_dtype=torch.float16, low_cpu_mem_usage=True)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model)
        #else:
         

    def setup(self):
        pass 

    def get_response(self):
        prompt = self.input_line

        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids
        gen_tokens = self.engine.generate(input_ids, do_sample=True, temperature=0.001, max_length=10,)
        gen_text = self.tokenizer.batch_decode(gen_tokens)[0]
        
        if gen_text.startswith(prompt):
            gen_text = gen_text[len(prompt):]
        gen_text = gen_text.strip()
        return gen_text
        

class GPTPipeline(DefaultGPT):
    def __init__(self, model):
        DefaultGPT.__init__(self)
        self.model = model
        self.file_name = args.tabname.split('.')[0] + '.' + args.model + ".query.tsv"
        self.input_line = "Hello there."
        self.is_online = True

        self.config = dotenv_values("../.env")
        #print(self.config)

        self.url = 'https://api.pipeline.ai/v2/runs'
    def setup(self):
        pass

    def get_response(self):
        prompt = self.input_line
        self.payload = {
                    "pipeline_id": self.model,
                    "blocking": False,
                    "compute_type": "gpu",
                    "data": [
                            prompt,
                            {
                                "response_length": 5, 
                                "include_input": False, 
                                "temperature": 0.00001, 
                                #"top_k": 5
                                }
                        ]
                }

        self.header = {
                    "Authorization": "Bearer " + self.config["PIPELINE_API_KEY"],
                    "Content-Type": "application/json"
                }
        gen_text = requests.post(self.url, json=self.payload, headers=self.header)
        gen_text = gen_text.text
        gen_text = json.loads(gen_text)
        gen_text = gen_text["result_preview"][0][0].strip()
        #print(gen_text , "<---")
        if gen_text.startswith(prompt):
            gen_text = gen_text[len(prompt):]
        gen_text = gen_text.strip()
        return gen_text
  

class GPT3(DefaultGPT):
    def __init__(self, model):
        DefaultGPT.__init__(self)
        self.model = model #"gpt3"
        self.file_name = args.tabname.split('.')[0] + '.' + args.model + ".query.tsv"
        self.input_line = "Hello there."
        self.is_online = True

        self.config = dotenv_values("../.env")
        #print(self.config)
        openai.api_key = self.config["OPENAI_API_KEY"]
        #self.organization = self.config["OPENAI_ORGANIZATION"]

    def setup(self):
        pass

    def get_response(self):
        gen_text = openai.Completion.create(
            model= self.model, #"text-davinci-002",
            prompt=self.input_line,
            max_tokens=5,
            temperature=0.0001
        )
        #print(gen_text , "<---")
        gen_text = gen_text["choices"][0]["text"].replace("\n","").strip()
        return gen_text

class HFOnline(DefaultGPT):
    def __init__(self, model):
        DefaultGPT.__init__(self)
        self.model = model #"gpt3"
        self.file_name = args.tabname.split('.')[0] + '.' + self.model.replace("/",".") + ".query.tsv"
        self.input_line = "Hello there."
        self.is_online = True

        self.API_URL = "https://api-inference.huggingface.co/models/" + self.model
        self.config = dotenv_values("../.env")
        #print(self.config)
        #openai.api_key = self.config["OPENAI_API_KEY"]
        self.bearer = self.config["HF_BEARER"]
        self.headers = {"Authorization": "Bearer " + self.bearer}
        #print(self.model,"untouched")

    def setup(self):
        pass

    def get_response(self):
        payload = { "inputs": self.input_line } #, config : {"max_length": 5 , "temperature": 0.00001}}
        #print(payload)

        response = requests.post(self.API_URL, headers=self.headers, json=payload)

        gen_text = response.json()[0]["generated_text"].replace("\n","").strip()
        if gen_text.startswith(self.input_line):
            gen_text = gen_text[len(self.input_line):]
        gen_text = gen_text.strip()
        
        return gen_text
        
class Checkpoint(DefaultGPT):
    def __init__(self, model):
        DefaultGPT.__init__(self)
        self.model = model #"gpt3"
        self.file_name = args.tabname.split('.')[0] + '.' + self.model.replace("/",".") + ".query.tsv"
        self.input_line = "Hello there."
        self.is_online = False

        path = str(os.environ.get("GPT_ETC_CHECKPOINT"))
        print(path)
        self.happy_gen = HappyGeneration( model_type="GPT-NEO", model_name=self.model, load_path=path )


    def setup(self):
        pass

    def get_response(self):
        args = GENSettings(max_length=15)
        result = self.happy_gen.generate_text(self.input_line, args=args)    
        print(result)
        print(result.text)  
        gen_text = result.text.strip()

        if gen_text.startswith(self.input_line):
            gen_text = gen_text[len(self.input_line):]
        gen_text = gen_text.strip()
        
        return gen_text


if __name__ == "__main__":
    skip = False
    gpt = DefaultGPT()

    if args.model == "gpt2":
        print("gpt2 model")
        try:
            gpt = GPT2("gpt2")
        except:
            skip = True
    elif args.model == "gptj":
        print("gptj model")
        #try:
        gpt = GPTJ("EleutherAI/gpt-j-6B")
        #except:
        #    skip = True
    elif args.model == "gpt3":
        print("gpt3 model")
        try:
            gpt = GPT3("text-davinci-002")
        except:
            skip = True
    elif args.model == "gpt3-curie":
        print("gpt3-curie")
        try:
            gpt = GPT3("text-curie-001")
        except:
            skip = True
    elif args.model == "gpt3-babbage":
        print("gpt3-babbage")
        try:
            gpt = GPT3("text-babbage-001")
        except:
            skip = True
    elif args.model == "gptj-pipeline":
        #print("pipeline")
        try:
            config = dotenv_values("../.env")["PIPELINE_MODEL_KEY_GPTJ"]
            gpt = GPTPipeline(config)
        except:
            skip = True
    elif args.huggingface != None:
        print("Huggingface model", args.huggingface)
        try:
            gpt = GPT2(args.huggingface)
        except:
            skip = True
    elif args.model.startswith("gpt2-"):
        print(args.model, "model")
        try:
            gpt = GPT2(args.model)
        except:
            skip = True
    elif args.online is False:
        print(args.model, "model using GPT2 framework and Huggingface")
        try:
            gpt = GPT2(args.model)
        except:
            skip = True
    elif args.checkpoint is True:
        print(args.model, "checkpoint")
        try:
            gpt = Checkpoint(args.model)
        except:
            skip = True
    else:
        print(args.model, "Huggingface online")
        try:
            gpt = HFOnline(args.model)
        except Exception as e:
            print(e)
            skip = True 


    gpt.setup()

    #print(gpt.model)
    print("names:", gpt.file_name, args.tabname)

    gpt.file_name = gpt.file_name.replace("/",".")
    
    if not exists("../data/" + gpt.file_name):
        save = open("../data/" + gpt.file_name.replace("/","."), "w")
        file = open("../data/" + args.tabname.replace("/","."), "r")
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
                        l[1] = l[1].replace("\n","").replace("\r","")
                    except  KeyboardInterrupt:
                        l[1] = ""
                        skip = True
                    '''
                    except Exception as e :
                        print(e)
                        l[1] = ""
                        if not gpt.is_online: skip = True
                        crash_count += 1 
                        if crash_count >= args.crashes: 
                            skip = True
                    '''
                else:
                    l[1] = ""
                
                if args.screen: print(num + 1, l[0], ">>" , l[1])
            x.append([ l[0], l[1] ])
            num += 1 
            if num >= args.length: break

        resave = open("../data/" + gpt.file_name, "w")
        for l in x:
            resave.write(l[0].strip() + "\t" + l[1].strip() + "\n")
        resave.close()
