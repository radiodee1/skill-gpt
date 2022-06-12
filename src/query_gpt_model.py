#!/usr/bin/env python3

import argparse
import sys

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
            return ""

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
        self.file_name = "gpt2"
        self.input_line = "Hello there."
        self.url = "https://"
        self.header = {}
        self.body = {}


class GPTJ(DefaultGPT):
    def __init__(self):
        DefaultGPT.__init__(self)
        self.model = "gptj"
        self.file_name = "gptj"
        self.input_line = "Hello there."
        self.url = "https://"
        self.header = {}
        self.body = {}


class GPT3(DefaultGPT):
    def __init__(self):
        DefaultGPT.__init__(self)
        self.model = "gpt3"
        self.file_name = "gpt3"
        self.input_line = "Hello there."
        self.url = "https://"
        self.header = {}
        self.body = {}




if __name__ == "__main__":
    gpt = DefaultGPT()

    if args.model == "gpt2":
        print("gpt2")
        gpt = GPT2()
    elif args.model == "gptj":
        print("gptj")
        gpt = GPTJ()
    elif args.model == "gpt3":
        print("gpt3")
        gpt = GPT3()

    gpt.setup()

    print(gpt.model)
    print(gpt.file_name)
