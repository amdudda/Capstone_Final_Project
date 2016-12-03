'''
Downloads images based on a url passed to code.
WARNING: assumes the url has been vetted by Django form validation.
'''
from PIL import Image
from ImageValidator import isImage
import time

def FetchImage(url,directory="."):
    '''
    Downloads and saves an image
    :param url: The URL of the image to be downloaded
    :param directory: the directory where the image is to be saved.
    :return: True if successful, False otherwise.
    '''

    # before we do anything else, make sure the url really does look like an image file.
    isAnImage, ErrMsg = isImage(url)

    if isAnImage:
        # let's establish the image filename and storage location
        img_fname = getFileName(url)
        print(img_fname)
        return True
    else:
        return False


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
    # dt = datetime.now()
    # ts_arr = [dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second]
    # for el in range(len(ts_arr)):
    #     ts_arr[el] = str(ts_arr[el])
    # ts = "_".join(ts_arr) + "_""
    format = "%Y%m%d%H%M%S_"
    ts = time.strftime(format)
    img_fname = ts + img_fname
    return img_fname


if __name__ == "__main__":
    testurl = 'http://www.aljazeera.com/mritems/assets/images/aj-logo-lg.png'
    FetchImage(testurl)