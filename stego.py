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
    parser.add_argument("--extract", help = "the file you want to print the hidden message to", type = str)
    parser.add_argument("--test", help = "used for testing, disregard", type = str)
    argv = parser.parse_args()

    # determine if a carrier file exists
    global png_flag
    try:
        with open(argv.carrier, 'rb') as carrier: # determine if it's a png
            c = carrier.read()[:8]
            if(c == png_marker):
                png_flag = 1
            else:
                png_flag = 0
    except:
        print("ERROR: carrier file specified not found")
        exit(1)

    # handle any argument given
    if argv.embed:
        embed_call(argv.embed, argv.carrier)
    elif argv.extract:
        extract_call(argv.extract, argv.carrier)
    elif argv.test:
        test_call(argv.test)
    elif(not (argv.embed or argv.extract)):
        print('No arguments specified.\nPlease select --embed or --extract')
        print('Use -h or --help for usage')
        exit(1)


# define my own global magic numbers
png_flag = -1 # flag if an image is a png to use more specific rules
png_marker = b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a' # marker that exists at the start of png files

sof = b'\xaa\xbb\xcc\xdd\xee\xff\xab\xcd'  # my own starting marker
eof = b'\xaa\xbb\xcc\xdd\xee\xff\xcd\xab'  # swapped last 2 bytes


# method to embed a message in carrier file
def embed_call(emb_msg, carrier):
    if(png_flag):
        embed_png(emb_msg, carrier)
        return

    print('you have selected embed')
    print('message to embed is: "{}"'.format(emb_msg)) # echo embed message

    g = str.encode(emb_msg, 'utf-8') # encoded message
    g = sof + g + eof # wrap file between magic numbers
    with open(carrier, 'rb') as m:
        f = m.read()  # read the raw binary
        mod_file = f + g  # append my message to the end
    # print(mod_file[-20:])
    mod_file_name = 'embed.' + carrier # generate new file name
    with open(mod_file_name, 'wb+') as f: # open or create file with embedded message
        f.write(mod_file)
    collect_data(carrier, mod_file_name) # gather and print data
    return


# method to extract message from a carrier file
def extract_call(ext_file, carrier):
    if(png_flag):
        extract_png(ext_file, carrier)
        return

    mnl = len(sof) # length of the magic numbers
    print('you have selected extract')
    with open(carrier, 'rb') as f: # read binary of the modified file
        r = f.read()
        e = r[r.find(sof)+mnl : r.find(eof)] # bytestring of the embeded message
        # print(e.decode('ascii')) # decoded, human-readable message
    mod_file_name = ext_file
    with open(mod_file_name, 'w') as f: # open or create plaintext file
        f.write(e.decode('ascii')) # write decoded message to file
        f.write('\n')
    remove_extract(carrier) # call method to remove extracted message from file


#remove extracted message from carrier
def remove_extract(carrier):
    # print(carrier)
    mnl = len(sof) # length of my magic numbers
    # print('mnl: {}'.format(mnl))
    with open(carrier, 'rb+') as f: # open file in binary
        r = f.read()
        critical = r[r.find(sof) : r.find(eof)+mnl] # section of data that contains hidden message and sof/eof markers
        w = r.replace(critical, b'') # remove selected section, replace with embty bytestring
        f.write(w)
    return



# embed method for png files
def embed_png(emb_msg, carrier):
    print('embed_png called')
    eml = len(emb_msg) # length of embed message
    n_bytes = 4  # want to represent eml in 4 bytes

    eml = eml.to_bytes(n_bytes, byteorder = 'big')  # converts length of my message to bytestring
    p_type = b'JAYY'  # custom type for new png chunk
    msg = str.encode(emb_msg, 'UTF-8')  # encoded message
    crc = binascii.crc32(p_type + msg).to_bytes(4, byteorder = 'big')  # some wacky thing that makes pngs work

    # full message to embed:
    # b'<length of message (4 bytes)> <TYPE> <message> <crc32>'
    full = eml + p_type + msg + crc  # full message I can put directly into png file


    # embedding image after first IDAT chunk - results in corrupt image
    # with open(carrier, 'rb') as f:
    #     r = f.read()
    #     target = r.find(b'IDAT') - 4  # Want to put my image before the first IDAT chunk
    #     before = r[:target]
    #     after = r[target:]
    #     r = before + full + after  # area to put my message
    # with open('new.png', 'wb') as f:
    #     f.write(r)

    # embedding image after last TDAT chunk - no image loss
    with open(carrier, 'rb') as f:
        r = f.read()
        target = r.rfind(b'IDAT')  # start of chunk type sector
        cdl = int.from_bytes(r[target-4:target], byteorder = 'big')  # chunk data length
        # print(cml)
        target = target + cdl + 4  # read from start of chunk type to end of chunk
        before = r[:target]
        after = r[target:]
        a = before + full + after  # area to put my message
    with open('new.png', 'wb') as f:
        f.write(a)


def extract_png(ext_file, carrier):
    print('called extract_png')
    tag = b'JAYY'  # tag to look for, start of the JAYY chunk type
    with open(carrier, 'rb+') as f:
        r = f.read()
        target = r.rfind(tag)
        print(r[target:])
        cdl = int.from_bytes(r[target-4:target], byteorder = 'big')  # chunk data length
        soc = target - 4
        eoc = target + 4 + cdl + 4
        critical = r[soc : eoc]  # hidden message chunk
        h_msg = r[target + 4 : eoc - 4]  # hidden messages
        print(h_msg.decode('ascii'))
        w = r.replace(critical, b'')
        f.write(w)
    with open(ext_file, 'w+') as f:
        f.write(h_msg.decode('ascii'))
        f.write('\n')








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
    global sof, eof, png_flag
    mnl = len(sof) # magic number length
    with open(fil, 'rb') as image:
        f = image.read()
        r = f[:25]
        # print(r)

    ftf = 'embed.' + fil
    print(ftf)
    with open(ftf, 'rb') as tft:
        s = tft.read()
        print(s[-20:])

    # print('png? {}'.format(png_flag))

    # png_marker = b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a'
    # print(f[:8] == png_marker)


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
