# Jay Hayward
# CYBR 5830-013
# Project 2

from hashlib import md5
from _md5 import md5
import os
import sys
import binascii
import string
from argparse import ArgumentParser

def main():

    parser = ArgumentParser(description = "This program will extract or embed a hidden message from a given file")
    parser.add_argument("carrier", help = "the carrier file you want to interact with", type = str)
    parser.add_argument("--embed", help = "the hidden message you want to embed into the carrer file", type = str)
    parser.add_argument("--extract", help = "the file you want to extract a message from", type = str)
    parser.add_argument("--test", help = "used for testing", type = str)
    argv = parser.parse_args()

    # determine if a carrier file exists
    try:
        carrier = open(argv.carrier)
        # print('carrier file is: "{}"'.format(argv.carrier))
    except:
        print("ERROR: carrier file specified not found")
        return

    # handle any argument given
    if argv.embed:
        embed_call(argv.embed, argv.carrier)
    elif argv.extract:
        extract_call(argv.extract, argv.carrier)
    elif argv.test:
        test_call(argv.test)
    else:
        # print('You should specify an argument. \nUse -h to see how to use my program')
        collect_data(argv.carrier, None)


def embed_call(emb_msg, carrier):
    # print('embed called')
    print('message to embed is: "{}"'.format(emb_msg))

    # print(str.encode(emb_msg, 'utf-8'))
    g = str.encode(emb_msg, 'utf-8')

    with open(carrier, 'rb') as m:
        f = m.read()
        mod_file = f + g
    # print(mod_file[-20:])
    mod_file_name = carrier+'.embed'
    with open(mod_file_name, 'wb+') as f:
        f.write(mod_file)
    collect_data(carrier, mod_file_name)


def extract_call(ext_file, carrier):
    print('extract called')
    try:
        f = open(ext, 'r')
        print('the file to extract from is "{}"'.format(ext))
    except:
        print("ERROR: extract file specified not found")
        return


# Gather data of original and modified file
def collect_data(og_file, mod_file):
    # print('collect called')
    st1 = os.stat(og_file)
    if not mod_file:  # collect just the data of the original file
        # print('no mod file')
        print('the size of original file "{}" is {}'.format(og_file, st1.st_size))
    else:
        print('mod file found')
        st2 = os.stat(mod_file)
        print('the size of original file "{}" is {} and'.format(og_file, st1.st_size))
        print('the size of the modified file "{}" is {}'.format(mod_file, st2.st_size))



def test_call(fil):
    with open(fil, 'rb') as image:
        f = image.read()
        r = f[-25:]
        print(r)







if __name__ == "__main__":
    main()
