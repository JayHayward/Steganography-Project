Jay Hayward

Steganography-Project

Project 3 for CYBR 5830-013 Digital Forensics



### WRITEUP

This program extracts and embeds strings within files so that messages can be sent discretely without being easy to read and decipher.
My initial strategy to this project was to simply append a message to the end of a given image file. This was easy enough to do, just encode my message, open the file, write it to the end, then re-encode the new file. This created no visible changes to the image and the message could be read with any text editor.
To extract a message, I had to take a more sophisticated approach, as to extract the message and only the message. To achieve this, I created my own magic numbers, written as bytestrings, to denote the start and end of my file. The SOF and EOF markers are both 8 bytes long, with the last 2 bytes swapped to distinguish them.
Before encoding a message, I first wrap the message in my markers. This makes my message easy to find in any file. To extract the message I take the string between the markers and print it to a new file. I then take the message including the markers and strip it from the file. This leaves me with a carrier file identical to the original.
In theory, because of my magic number method, one should be able to hide a secret message in any file at any location, while still making it easy to extract. This method works for most file types.

The second part of this project involved PNG files. PNG files are very interesting in the way that they are written and how computer interpret the information.
The reason I decided to look at PNG files is because, after some research, the structure of the files allowed new information to be inserted within the code, between different chunks in the image.
In my program, when command line input is first passed in, I parse the file information, and set a flag to show if a file was a PNG or not. If a function is executed and the flag is set to 1, it jumps to a special version of the function.
PNG files consist of a lot of chunks, all with different functions for the image. In order to embed an image in a way that it can be easily found and extracted, I wanted to place my image next to a data chunk, which contains actual image data. They are easy to find due to their structure and clear "IDATA" tag in the binary.
Data chunks consist of 4 sections: a 4-byte data size descriptor, a 4-byte type label, a variable-size data section, and a 4-byte crc32 section. I won't go into detail about these different sections, the important bit is that the first 4 bytes determine the size of the data, and therefore determines size of the chunk. When embedding my message I had to take chunk size into consideration and use offsets accordingly.
The interesting thing about embedded messages in PNGs is that, if you're clever about it, you can embed or extract a message of any size without altering the image at all. After a few attempts of putting messages different places, I arrived at the conclusion that placing a string after the terminal data chunk would successfully hide the image, as well as keep the image in-tact.

For further information on how I'm going about this project, the commented code should be enough to give you a good understanding of my methods. 


# TO RUN MY SCRIPT:

python stego.py -h                                      to receive information about and how to use my program__
python stego.py <carrier>                               asks you to specify an argument and shows usage__
python stego.py <carrier> --embed <message>             takes a message string and embeds it in the carrier file
                                                          this will result in a file named embed.<carrier>__
python stego.py <carrier> --extract <filename>          takes the embedded file specified and extracts the message from it
                                                          this will result in a file with the specified filename containing                                                             the hidden message
