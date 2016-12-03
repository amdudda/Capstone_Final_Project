'''
Downloads images based on a url passed to code.
WARNING: assumes the url has been vetted by Django form validation.
'''
from PIL import Image
from ImageValidator import isImage
from os import path
from io import BytesIO
import time, requests

def FetchImage(url,directory="."):
    '''
    Downloads and saves an image
    :param url: The URL of the image to be downloaded
    :param directory: the directory where the image is to be saved.
    :return: file name if successful, False otherwise.
    '''

    # before we do anything else, make sure the url really does look like an image file.
    isAnImage, ErrMsg = isImage(url)

    if isAnImage:
        # let's establish the image filename and storage location
        img_fname = getFileName(url)
        img_file_path = path.join(directory,img_fname)
        # now that we have a file name, we need to fetch and save the image
        save_image(img_file_path, url)
        return img_fname
    else:
        return False


def save_image(img_file_path, url):
    # see http://stackoverflow.com/questions/24920728/convert-pillow-image-into-stringio#24920879 for leads on how to do this -- that url plus some other wrangling led me to use BytesIO to read and save the image.
    response = requests.get(url).content
    # print(response)
    retrieved_img = BytesIO(response)
    # then convert it into something savable and save it
    saveable_img = Image.open(retrieved_img)
    saveable_img.save(img_file_path)


def getFileName(url):
    '''
    returns a file name t
    :param url: Url of the source file
    :return: string with a file name prepended by a timestamp
    '''
    index = url.rfind('/') + 1
    img_fname = url[index:]
    # get the last 100 characters only, prepend it with a timestamp to ensure high likelihood of unique filenames
    img_fname = img_fname[-100:]
    format = "%Y%m%d%H%M%S_"
    ts = time.strftime(format)
    img_fname = ts + img_fname
    return img_fname


if __name__ == "__main__":
    testurl = 'http://www.aljazeera.com/mritems/assets/images/aj-logo-lg.png'
    print(FetchImage(testurl))