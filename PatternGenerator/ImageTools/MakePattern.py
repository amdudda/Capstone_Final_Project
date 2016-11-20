'''
    PIL documentation at http://www.effbot.org/imagingbook/image.htm
'''
from PIL import Image

# static value - an array of possible characters to use as replacements for rgb tuples
SYMBOLS = ['@','#','$','%',
           '&','*','+','<',
           'ß','?','=','<',
           '€','‡','µ','/',
           '÷']  # 'divided by' is a debugging character to flag that more than 16 colors were generated

'''
Workflow:

take an image, generate a bitmap, convert bitmap to pattern, save bitmap to file, save file location & pattern data to database

tools needed: image converter & resizer, bitmap parser, histogram generator, convert rgb tuples to symbols, store pattern.

to be done in a separate utility: parse stored pattern into human-readable format for display on web page; convert pattern from flat knit to ribbed/garter stitches; add borders

'''

def image2bitmap(src,farben=16):
    '''
    takes an image and returns a bitmap
    :param src: image that PIL.Image can understand and convert to bitmap
    :param farben: number of colors to compress image down to.
    :return: a bitmap image
    '''
    src_img = Image.open(src)
    bmp_img = src_img.quantize(colors=farben, method=None, kmeans=0, palette=None)
    return bmp_img

def get_pixels(img):
    '''
    takes a bitmap and returns the images's pixels as an array
    :param img: a bitmap image
    :return: an array of rgb tuples
    '''
    return list(img.getdata())

def get_unique_colors(colorlist):
    '''
    takes a array of colors and returns a list of unique colors
    :param colorlist: a list of rgb tuples
    :return: a list of unique rgb tuples
    '''
    unique_vals = []
    for t in colorlist:
        if t not in unique_vals: unique_vals.append(t)
    return unique_vals

def colors_to_symbols(colors):
    '''
    takes a list of colors and returns a dictionary assigning each color to a symbol
    :param colors: a list of rgb tuples
    :return: a dictionary mapping rgb tuples to a symbol
    '''
    colormap = {}
    for i in range(len(colors)):
        colormap[colors[i]] = SYMBOLS[i]
    return colormap


# debugging
if __name__ == "__main__":
    test_img = '../static/images/source/2016-11-18-12-51_sunflowers-1719119_150.jpg'
    # test_src = Image.open(test_img)
    my_bmp = image2bitmap(test_img)
    my_pixels = get_pixels(my_bmp)
    my_colorlist = get_unique_colors(my_pixels)
    ## these just print lists of numbers, not the corresponing RGB tuples
    print(my_pixels)
    print(my_colorlist)
    # some data as I continue to debug:
    print(my_bmp.height)
    print(my_bmp.width)