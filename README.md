Jay Hayward

Steganography-Project

Project 3 for CYBR 5830-013 Digital Forensics



WRITEUP

This program extracts and embeds strings within files so that messages can be sent discretely without being easy to read and decipher.
My initial strategy to this project was to simply append a message to the end of a given image file. This was easy enough to do, just encode my message, open the file, write it to the end, then re-encode the new file. This created no visible changes to the image and the message could be read with any text editor.
To extract a message, I had to be more sophisticated, as to extract the message and only the message. To achieve this, I created my own magic numbers, written in hex, to denote the start and end of my file. The sof and eof markers are both 8 bytes long, with the last 2 bytes swapped to distinguish them.
Before encoding a message, I first wrap the message in my markers. This makes my message easy to find in any file. To extract the message I take the string between the markers and print it to a new file. I then take the message including the markers and strip it from the file. This leaves me with a carrier file identical to the original.


TO RUN MY SCRIPT:

python stego.py -h                                      to receive information about and how to use my program
python stego.py <carrier>                               prints information about the carrier file and asks you to specify an argument
python stego.py <carrier> --embed <message>             takes a message string and embeds it in the carrier file
                                                        this will result in a file named <carrier>.embed
python stego.py <carrier> --extract <embed_file>        takes the file specified and extracts the message from it
                                                        this will result in two files:
                                                            <carrier>.extract - a text file containing the hidden message
                                                            <carrier>.removed - the carrier file after a hidden message is extracted. It will be identical to the original carrier file

diff -s <carrier> <carrier>.removed                     confirms that the original carrier file and the .removed file are identical


In theory, because of my magic number method, one should be able to hide a secret message in any file at any location, while still making it easy to extract, without affecting the carrier file.
