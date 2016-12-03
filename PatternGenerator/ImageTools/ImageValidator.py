from PIL import Image
from urllib.parse import urlparse
import mimetypes,httplib2

# cribbed from https://timmyomahony.com/blog/upload-and-validate-image-from-url-in-django/

VALID_IMAGE_EXTENSIONS = [
    # abstracted from http://pillow.readthedocs.io/en/3.0.x/handbook/image-file-formats.html
    ".bmp",
    ".eps",
    ".gif",
    ".jpg",
    ".jpeg",
    ".png",
    ".tiff",
]
VALID_IMAGE_MIMETYPES = [ "image" ]
VALID_SIZE = 9999  # this is a reasonableness check, as no one will want to knit a 1000-inch wide item!!!

def isImage(url):
    '''
    Takes a URL and verifies it actually points to an image. This method assumes the URL has already been vetted as being url-like by a Django form
    :param url: the URL where the image is located
    :return: (boolean, string) tuple. The boolean element is True if it passes tests, False if not. The string element is an empty string if the boolean is True, and contains error information if the boolean is False.
    '''

    if not valid_url_extension(url):
        return (False, "The file does not appear to have a valid file extension")
    elif not valid_url_mimetype(url):
        return (False, "The URL's mimetype information is not consistent with an image file.")
    elif not image_exists(url):
        return (False, "The image does not appear to exist on the server.")
    else:
        # looks like we have a winner!
        return (True, "")
# end isImage


''' SUPPORTING METHODS FOR isImage() '''
# AMD: vets that the url appears to tpoint to a valid file type extension.
def valid_url_extension(url, extension_list=VALID_IMAGE_EXTENSIONS):
    # http://stackoverflow.com/a/10543969/396300
    url=url.lower()  # AMD set url to lowercase b/c extension validity is not case-sensitive
    return any([url.endswith(e) for e in extension_list])
# end valid_url_extension

# checks the mimetype metadata - not sure what the point is if it passes known good file extensions with invalid mimetypes?
# TODO: create something that truly does defend against invalid MIME types.
def valid_url_mimetype(url, mimetype_list=VALID_IMAGE_MIMETYPES):
    # http://stackoverflow.com/a/10543969/396300
    mimetype, encoding = mimetypes.guess_type(url)

    if mimetype:
        return any([mimetype.startswith(m) for m in mimetype_list])
    else:
        return False
# end valid_url_mimetype

# verifies the file actually exists on the target server.
def image_exists(url): #domain, path):
    # http://stackoverflow.com/questions/2486145/python-check-if-url-to-jpg-exists

    #AMD: need to parse out domain and path.  https://docs.python.org/2/library/urlparse.html
    parsed_url = urlparse(url)
    domain,path = urlparse(url).netloc, urlparse(url).path
    # print(domain)
    # print(path)

    # AMD: then back to borrowed code
    try:
        conn = httplib2.HTTPConnectionWithTimeout(domain)
        conn.request('HEAD', path)
        response = conn.getresponse()
        conn.close()
    except Exception as e:
        # print(e)
        return False
    return response.status == 200
# end image_exists

''' OTHER VALIDATORS '''
def isValidSize(image):
    # validates that the image is smaller or equal to maximum size.
    img_width = image.width
    img_height = image.height
    return (img_width <= VALID_SIZE and img_height <= VALID_SIZE)

''' DEBUGGING '''
if __name__ == "__main__":
    test_set = {
        'bad_ext' : "file.ico",
        'malicious_ext' : "file.exe",
        'bad_mimetype' : "http://entropymine.com/jason/testbed/mime/oct/file.png",
        'file_dne' : "http://pixabay.com/zzz.jpg",
        'really_an_image' : "http://www.aljazeera.com/mritems/assets/images/aj-logo-lg.png",
    }
    # test_set = [bad_ext,malicious_ext,bad_mimetype,file_dne,really_an_image]
    for key in test_set:
        print(key, isImage(test_set[key]))

