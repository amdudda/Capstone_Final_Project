'''
    PIL documentation at http://www.effbot.org/imagingbook/image.htm
'''
from PIL import Image
import webcolors

# static value - an array of possible characters to use as replacements for rgb tuples
# can't use (, ), or * - they're reserved symbols used for noting repetitions in a pattern
SYMBOLS = ['@','#','$','%',
           '&','÷','+','<',
           'ß','?','=','>',
           '€','‡','µ','/',
           '!']  # '!' is a debugging character to flag that more than 16 colors were generated

'''
Workflow:

take an image, generate a bitmap, convert bitmap to pattern, save bitmap to file, save file location & pattern data to database

tools needed: image converter & resizer, bitmap parser, histogram generator, convert rgb tuples to symbols, store pattern.

to be done in separate utilities: parse stored pattern into human-readable format for display on web page; convert pattern from flat knit to ribbed/garter stitches; add borders; rgb to hex color conversion

'''

# TODO : rescale image before converting to bitmap
def image2bitmap(src,farben=16):
    '''
    takes an image and returns a bitmap
    :param src: image that PIL.Image can understand and convert to bitmap
    :param farben: number of colors to compress image down to.
    :return: a bitmap image
    '''
    src_img = Image.open(src)
    bmp_img = src_img.quantize(colors=farben, method=None, kmeans=0, palette=None).convert(mode="RGB")
    return bmp_img

def get_pixels(img):
    '''
    takes a bitmap and returns the images's pixels as an array
    :param img: a bitmap image
    :return: an array of rgb tuples
    '''
    # myimg = img.convert(mode="RGB")
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
    # get_colour_name = get_closest_CSS_color()

    colormap = {}
    for i in range(len(colors)):
        cur_color = colors[i]
        cur_symbol = SYMBOLS[i]
        nearest_webcolor = get_closest_CSS_color(cur_color)
        # color_name = webcolors.rgb_to_name(nearest_webcolor)
        colormap[cur_color] = [cur_symbol, nearest_webcolor]
    return colormap


def get_closest_CSS_color(color_tuple):
    # calculate nearest web-safe color and store a micro-array with symbol and css name
    # http://stackoverflow.com/questions/9694165/convert-rgb-color-to-english-color-name-like-green#9694246
    def closest_colour(requested_colour):
        min_colours = {}
        for key, name in webcolors.css3_hex_to_names.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_colour[0]) ** 2
            gd = (g_c - requested_colour[1]) ** 2
            bd = (b_c - requested_colour[2]) ** 2
            min_colours[(rd + gd + bd)] = name
        return min_colours[min(min_colours.keys())]

    def get_colour_name(requested_colour):
        try:
            closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
        except ValueError:
            closest_name = closest_colour(requested_colour)
            actual_name = None
        return actual_name, closest_name

    return get_colour_name(color_tuple)[1]


def make_pattern(img_pixels,color_key):
    '''
    generates a string corresponding to a flat knitting pattern
    :param img_pixels: list of all the pixels in the bitmap
    :param color_key: a dictionary mapping color values to ASCII symbols
    :return: string representing a flat knitting pattern
    '''
    output = ''
    for c in img_pixels:
        symbol = color_key[c]
        output += symbol[0]
    return output

def pattern_as_array(patt,i_h,i_w):
    pattern_arr = []
    for r in range(i_h):
        rowdata = ""
        for s in range(i_w):
            rowdata += patt[(r*i_w) + s]
            # want to break things up into groups of 5 stitches - this works, sort of, but needs to happen later in processing
            # to prevent odd ends if rows don't happen to be in multiple of 5
            if s > 0 and (s+1)%5==0: rowdata += " "
        if r%2 == 1:
            # if a wrongside row, need to reverse string sequence so that correct stitches get made
            # http://stackoverflow.com/questions/931092/reverse-a-string-in-python
            rowdata = "purl row:\t" + rowdata[::-1].strip()
        else:
            rowdata = "knit row:\t" + rowdata
        # print(rowdata)
        pattern_arr.append(rowdata)
    return pattern_arr

def get_image_data(filename):
    '''
    crunch a bunch of numbers and return a dictionary of data that can be appended to a context object.
    :param filename: the filename of the bitmap used to generate the pattern's image
    :return: dictionary containing number of colors, color data, and a pattern string.
    '''
    # load the image we want to work with
    import os
    # fpath = "../static/images/bitmaps/" +
    fpath = os.path.join('PatternGenerator','static','images','bitmaps', filename)
    bmp_img = Image.open(fpath)

    # collect data about the image

    # bmp_img = my_bmp.convert(mode="RGB")
    my_pixels = get_pixels(bmp_img)
    my_colorlist = get_unique_colors(my_pixels)
    my_colordict = colors_to_symbols(my_colorlist)
    patt_string = make_pattern(my_pixels, my_colordict)
    my_pattern = pattern_as_array(patt_string,bmp_img.height,bmp_img.width)

    # compile the info into a dictionary object
    pattern_data = {
        'colors' : len(my_colorlist),
        'map_symbols_to_colors': my_colordict,
        'pattern_array': my_pattern
    }

    #return the data
    return pattern_data
#end get_image_data

# debugging
if __name__ == "__main__":
    test_img = '../static/images/source/woodcarving.jpeg'
    # test_src = Image.open(test_img)
    my_bmp = image2bitmap(test_img,farben=16)
    my_bmp.save("../static/images/bitmaps/wingedlady_5_5_16.bmp")
    my_pixels = get_pixels(my_bmp)
    my_colorlist = get_unique_colors(my_pixels)
    print(my_pixels[:16])
    print("colors generated: " + str(len(my_colorlist)))
    # for c in my_colorlist:
    #     print(c)
    my_colordict = colors_to_symbols(my_colorlist)
    cd_keys = my_colordict.keys()
    # for k in cd_keys:
    #     print(str(k) + ": " + my_colordict[k])
    # my_pattern = make_pattern(my_pixels,my_colordict)
    # i_w = my_bmp.width
    # i_h = my_bmp.height
    # print_pattern(my_pattern,my_bmp.height,my_bmp.width)

    # print(my_pattern)