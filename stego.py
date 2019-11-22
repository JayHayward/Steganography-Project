# Jay Hayward
# CYBR 5830-013
# Project 3

from hashlib import md5
from _md5 import md5
import os
import sys
import binascii
import string
import random
from argparse import ArgumentParser

def main():

    parser = ArgumentParser(description = "This program will extract or embed a hidden message from a given file")
    parser.add_argument("carrier", help = "the carrier file you want to interact with", type = str)
    parser.add_argument("--embed", help = "the hidden message you want to embed into the carrer file", type = str)
    parser.add_argument("--extract", help = "the file you want to extract a message from", type = str)
    parser.add_argument("--test", help = "used for testing, disregard", type = str)
    argv = parser.parse_args()

    # determine if a carrier file exists
    try:
        carrier = open(argv.carrier)
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
        collect_data(argv.carrier, None) # print data if no argument is specified


# define my own global magic numbers
sof = b'\xaa\xbb\xcc\xdd\xee\xff'  # my own starting marker
eof = b'\xaa\xbb\xcc\xdd\xff\xee'  # swapped last 2 bytes


# method to embed a message in carrier file
def embed_call(emb_msg, carrier):
    global sof, eof
    print('you have selected embed')
    print('message to embed is: "{}"'.format(emb_msg)) # echo embed message

    g = str.encode(emb_msg, 'utf-8') # encoded message
    g = sof + g + eof # wrap file between magic numbers
    with open(carrier, 'rb') as m:
        f = m.read()  # read the raw binary
        mod_file = f + g  # append my message to the end
    # print(mod_file[-20:])
    mod_file_name = carrier+'.embed' # generate new file name
    with open(mod_file_name, 'wb+') as f: # open or create file with embedded message
        f.write(mod_file)
    collect_data(carrier, mod_file_name) # gather and print data
    return


# method to extract message from a carrier file
def extract_call(ext_file, carrier):
    global sof, eof
    mnl = len(sof) # length of the magic numbers
    print('you have selected extract')
    with open(ext_file, 'rb') as f: # read binary of the modified file
        r = f.read()
        # print(r[-30:])
        e = r[r.find(sof)+mnl : r.find(eof)] # bytestring of the embeded message
        print(e.decode('ascii')) # decoded, human-readable message
    mod_file_name = carrier+'.extract'
    with open(mod_file_name, 'w+') as f: # open or create plaintext file
        f.write(e.decode('ascii')) # write decoded message to file
        f.write('\n')
    remove_extract(ext_file, carrier) # call method to remove extracted message from file



def remove_extract(ext_file, carrier):
    global sof, eof
    mnl = len(sof) # length of my magic numbers
    with open(ext_file, 'rb') as f: # open file in binary
        r = f.read()
        critical = r[r.find(sof) : r.find(eof)+mnl] # section of data that contains hidden message and sof/eof markers
        w = r.replace(critical, b'') # remove selected section, replace with embty bytestring
        # print(w[-50:])
    mod_file_name = carrier+'.removed'
    with open(mod_file_name, 'wb+') as g: # open or create file, in binary
        g.write(w) # write to binary file so that it recreates the original image
    return



# Gather data of original and modified file
def collect_data(og_file, mod_file):
    # print('collect called')
    st1 = os.stat(og_file)
    if not mod_file:  # collect just the data of the original file
        print('no argument selected, printing data of the carrier file')
        print('the size of original file "{}" is {}'.format(og_file, st1.st_size))
        print('the md5 hash of the original file is {}'.format(md5(og_file.encode('ascii')).hexdigest()))
        print('type "python stego.py -h" to see possible commands')
    else:
        # print('mod file found')
        st2 = os.stat(mod_file)
        print('the size of original file "{}" is {}'.format(og_file, st1.st_size))
        print('the md5 hash of the original file is {}'.format(md5(og_file.encode('ascii')).hexdigest()))
        print('the size of the modified file "{}" is {}'.format(mod_file, st2.st_size))
        print('the md5 hash of the modified file is {}'.format(md5(mod_file.encode('ascii')).hexdigest()))
    return


# used for various testing. disregard
def test_call(fil):
    global sof, eof
    mnl = len(sof) # magic number length
    # with open(fil, 'rb') as image:
    #     f = image.read()
    #     r = f[-25:]
    #     print(r)

    # with open(fil, 'rb') as f:
    #     print(f.read()[-50:])
    #     r = f.read()
    #     print(r.find(sof))
    #     print(r.find(eof))
    #     print(r[r.find(sof)+mnl : r.find(eof)])
    #     a = r[r.find(sof)+mnl : r.find(eof)]_
    #     print(a.decode('ascii'))






if __name__ == "__main__":
    main()
