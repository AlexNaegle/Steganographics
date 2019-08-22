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
    childName = 'amon64x32'

    #load parent image, pixels, and dimensions
    parent = Image.open(parentName + '.png')
    parentPix = parent.load()
    pw, ph = parent.size

    #load child image, pixels, and dimensions
    child = Image.open(childName + '.png')
    childPix = child.load()
    cw, ch = child.size

    #display parent and child
    parent.show()
    child.show()

    #ask user for bit size
    bitSize = int(input("Bits to replace(1-8): "))

    #check bitSize is valid for parent and child images
    if bitSize < 1 or bitSize > 8:
        print("invalid input")
        exit()
    elif pw*ph < (4 + cw*ch) * (lsbCalc[bitSize]):
        print("parent image not large enough")
        exit()

    bigString = ""

    #13bit conversions for dimensions
    cwBin = bin(cw)[2:]
    chBin = bin(ch)[2:]

    #add zeros to length 13
    while cwBin.__len__() < 13 or chBin.__len__() < 13:
        if cwBin.__len__() < 13:
            cwBin = "0" + cwBin

        if chBin.__len__() < 13:
            chBin = "0" + chBin

    #string stores all values in child image, load it
    bigString = cwBin + chBin + "000000"

    for i in range(cw):
        for j in range(ch):
            red = dToB8(childPix[i, j][0])
            green = dToB8(childPix[i, j][1])
            blue = dToB8(childPix[i, j][2])
            bigString = bigString + red + green + blue

    #start hiding data in parent pixels
    offset = 0

    #iteration through parent pixels
    for i in range(pw):
        for j in range(ph):
            #get pixel data
            red = dToB8(parentPix[i, j][0])
            green = dToB8(parentPix[i, j][1])
            blue = dToB8(parentPix[i, j][2])

            #edit pixel data
            if offset < bigString.__len__():
                red = red[0: -bitSize] + bigString[offset: offset + bitSize]
                offset = offset + bitSize

                if offset < bigString.__len__():
                    green = green[0: -bitSize] + bigString[offset: offset + bitSize]
                    offset = offset + bitSize

                    if offset < bigString.__len__():
                        blue = blue[0: -bitSize] + bigString[offset: offset + bitSize]
                        offset = offset + bitSize

            #put pixel data back in
            parentPix[i, j] = (bToD8(red), bToD8(green), bToD8(blue))

    #show image
    parent.show()
    parent.save("C:/Users/Alex/PycharmProjects/csc520TermProject/" + parentName + "_hiding_" + childName + "_rate" + str(bitSize) + ".png", "PNG", quality=100, subsampling=0)
    print("file saved!")

#show hidden contents of loaded image


def reveal():
    #useful variables
    imgName = "wooky_hiding_eku_rate2"

    #load image
    img = Image.open(imgName + ".png")
    imgPix = img.load()
    iw, ih = img.size

    #ask user for input
    bitSize = int(input("Bits to replace(1-8): "))

    #check bitSize
    if bitSize < 1 or bitSize > 8:
        print("invalid input")
        exit()

    #string to store hidden data
    bigString = ""

    #extract hidden data from image
    for i in range(iw):
        for j in range(ih):
            red = dToB8(imgPix[i, j][0])
            green = dToB8(imgPix[i, j][1])
            blue = dToB8(imgPix[i, j][2])

            bigString = bigString + red[-bitSize:]
            bigString = bigString + green[-bitSize:]
            bigString = bigString + blue[-bitSize:]

    #get dimensions, convert dimensions, and store them
    wOutBin = bigString[:13]
    hOutBin = bigString[13:26]

    n = 0
    for i in range(0, 13):
        if wOutBin[i: i + 1] == "1":
            n = n + 2 ** (12 - i)

    wOut = n

    n = 0
    for i in range(0, 13):
        if hOutBin[i: i + 1] == "1":
            n = n + 2 ** (12 - i)

    hOut = n

    #create blank image with lifted dimensions
    output = Image.new('RGB', (wOut, hOut))
    outputPix = output.load()

    #remove first 32 bits from bigString, dimension numbers
    bigString = bigString[32:]

    #create tracking number
    offset = 0

    #load colors into it
    for i in range(wOut):
        for j in range(hOut):
            red = bToD8(bigString[offset:offset+8])
            offset = offset + 8

            green = bToD8(bigString[offset:offset + 8])
            offset = offset + 8

            blue = bToD8(bigString[offset:offset + 8])
            offset = offset + 8

            outputPix[i, j] = (red, blue, green)

    #show and save revealed image
    img.show()
    output.show()
    output.save("C:/Users/Alex/PycharmProjects/csc520TermProject/" + imgName + "_revealed_image_rate" + str(bitSize) + ".png", "PNG", quality=100, subsampling=0)
    print("file saved!")

def main():
    hide()

main()
