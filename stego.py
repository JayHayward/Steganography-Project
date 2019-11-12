# Jay Hayward
# CYBR 5830-013
# Project 2

import os
import sys
import binascii
import hashlib
import string
from argparse import ArgumentParser

def main():

    parser = ArgumentParser(description = "This program will extract or embed a hidden message from a given file")
    parser.add_argument("carrier", help = "the carrier file you want to interact with", type = str)
    parser.add_argument("--embed", help = "the hidden message you want to embed into the carrer file", type = str)
    parser.add_argument("--extract", help = "the file you want to extract a message from", type = str)
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
        embed_call(argv.embed)
    elif argv.extract:
        extract_call(argv.extract)
    else:
        # print('You should specify an argument. \nUse -h to see how to use my program')
        collect_data(argv.carrier, None)


def embed_call(emb):
    print('embed called')
    print('message to embed is: "{}"'.format(emb))


def extract_call(ext):
    print('extract called')
    try:
        f = open(ext, 'r')
        print('the file to extract from is "{}"'.format(ext))
    except:
        print("ERROR: extract file specified not found")
        return


# Gather data of original and modified file
def collect_data(og_file, mod_file):
    print('collect called')
    if not mod_file:  # collect just the data of the original file
        print('no mod file')
    else:
        print('mod found')








if __name__ == "__main__":
    main()
