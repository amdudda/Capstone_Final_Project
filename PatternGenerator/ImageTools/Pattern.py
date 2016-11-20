'''
    PIL documentation at http://www.effbot.org/imagingbook/image.htm
    this is just my buggy proof of concept code -- I will be recycling this to develop image processing utilitites.
'''
from PIL import Image

myimg = Image.open('../static/images/source/2016-11-18-12-51_sunflowers-1719119_150.jpg')
# print(myimg.getdata)
# myimg = myimg.convert(mode="RGB",colors=8) # compress image down to 16 colors if needed.
# myimg.convert(colors=2).save("test.bmp")

image_as_rgb_array = list(myimg.getdata())
revimg = image_as_rgb_array[:]
revimg.reverse()
# image_as_rgb_array.save("test.bmp")


img_width = myimg.size[0]
img_height = myimg.size[1]
print("image size is " + str(img_width) + " x " + str(img_height) + " pixels.\n")

newimg = myimg
# newimg.putdata(revimg)
# this converts the image to a 16-color image that we can then save to a bitmap
newimg = newimg.quantize(colors=16, method=None, kmeans=0, palette=None)
# we could use the next line to resize it to whatever dimensions we felt like.
# newimg = newimg.resize((img_width,img_height*2))
# newimg.save("test.bmp")

# print out a list of the pixels in the image
# want to print each row of the image separately - need to think this through, I don't think this loop works
for i in range(img_height):
    for j in range(img_width):
        print(image_as_rgb_array[(i*img_width) + j])
    print("\n")

# print out a list of the number of pixels of each color found.
# this doens't really get me what I want, which is a list of the actual colors used, but it's good validation
# that my image has been compressed down to 16 colors.
print(str(len(newimg.getcolors())) + " colors")
for c in newimg.getcolors():
    # color = str(c[1])
    color_count = str(c[0])
    print(str(c) + ": " + color_count + " pixels.")