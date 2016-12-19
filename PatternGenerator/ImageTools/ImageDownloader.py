'''
Downloads images based on a url passed to code.
WARNING: assumes the url has been vetted by Django form validation.
'''
from PIL import Image
from .ImageValidator import isImage, isValidSize
from os import path
from io import BytesIO
import time, requests

def FetchImage(url,directory=".",rotation=None):
    '''
    Downloads and saves an image
    :param url: The URL of the image to be downloaded
    :param directory: the directory where the image is to be saved.
    :param rotation: whether to rotate the image 90 degrees; True if yes, False or None if not.
    :return: a tuple containing (file name, image width, image height) if successful, False otherwise.
    '''

    # before we do anything else, make sure the url really does look like an image file.
    isAnImage, ErrMsg = isImage(url)

    if isAnImage:
        # let's establish the image filename and storage location
        img_fname = getFileName(url)
        img_file_path = path.join(directory,img_fname)
        # now that we have a file name, we need to fetch the image
        savable_image = download_image(url)
        # then we validate that the image's size is small enough to fit in our database before we actually save it
        if isValidSize(savable_image):
            if rotation:
                savable_image.rotate(90) # rotate 90 degrees counterclockwise
            savable_image.save(img_file_path)
            # return the file name so the file's metadata can be stored in the database
            # return height/width metadata, too
            while True:
                # check if the file is done writing - don't let code proceed until filewrite is done.
                try:
                    # try a quick open-close of the file - there will be an IOError if file still being written
                    file = open(img_file_path)
                    file.close()
                    break
                except:
                    print('file still writing')
                    # pass
            w = savable_image.width / 10
            h = savable_image.height / 10
            return (img_fname,w,h)
        else:
            return False
    else:
        return False


def download_image(url):
    '''
    pulls an image off the internet and returns an Image object
    :param url: URL where the image resides
    :return:  Python Pillow (PIL) Image object
    '''
    # see http://stackoverflow.com/questions/24920728/convert-pillow-image-into-stringio#24920879 for leads on how to do this -- that url plus some other wrangling led me to use BytesIO to read and save the image.
    response = requests.get(url).content
    # print(response)
    retrieved_img = BytesIO(response)
    # then convert it into something savable and save it
    return Image.open(retrieved_img)


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
    nuther_url = 'https://lisalarter.com/wp-content/uploads/2015/09/Focus-How-To-Prioritize-Complete-Big-Honking-Business-Projects-1200x675.jpg'
    print(FetchImage(nuther_url))