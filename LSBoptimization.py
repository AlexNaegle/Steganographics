#least significant bit steganography hiding and revealing tool
#written by Alex Naegle
#only works with .png
#hider checks if images can fit properly

#imports
from PIL import Image

#turn an 0-255 number to 8 bit binary
def dToB8(n):
    #output string
    binary = ""
    #known 8 bit number, run 8 times
    for i in range(0,8):
        #divide n by 2, save remainder to bin
        binary = str(n%2) + binary
        n = n//2
    return binary


#turn an 8 bit binary number(string) to decimal
def bToD8(s):
    #output n
    n = 0
    for i in range(0,8):
        if s[i: i+1] == "1":
            n = n + 2**(7-i)

    return n

#hide child image in parent image


def hide():
    #useful variables
    lsbCalc = {1: 8, 2: 4, 3: 2.67, 4: 2, 5: 1.67, 6: 1.34, 7: 1.34, 8: 1}
    parentName = 'throwup'
    childName = 'wooky'

    #load parent image, pixels, and dimensions
    parent = Image.open(parentName + '.png')
    parentPix = parent.load()
    pw, ph = parent.size

    #load child image, pixels and dimensions
    child = Image.open(childName + '.png')
    childPix = child.load()
    cw, ch = child.size()

    #display parent and child
    parent.show()
    child.show()

    #ask user for bit size
    bitSize = int(input("Bits to replace(1-8): "))

    #validate bitSize based on parent and child images
    if bitSize < 1 or bitSize > 8:
        print("invalid input")
        exit()
    elif pw*ph < (4 + cw*ch) * (lsbCalc[bitSize]):
        print("parent image not large enough")
        exit()

    #13bit conversions for dimensions
    cwBin = bin(cw)[2:]
    chBin = bin(ch)[2:]

    #add zeros to length 13
    while cwBin.__len__() < 13 or chBin.__len__() < 13:
        if cwBin.__len__() < 13:
            cwBin = "0" + cwBin

        if chBin.__len__() < 13:
            chBin = "0" + chBin