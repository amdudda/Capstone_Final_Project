import mimetypes,httplib2
from urllib.parse import urlparse

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

def isImage(url):
    '''
    Takes a URL and verifies it actually points to an image. This method assumes the URL has already been vetted as being url-like by a Django form
    :param url: the URL where the image is located
    :return: (boolean, string) tuple. The boolean element is True if it passes tests, False if not. The string element is an empty string if the boolean is True, and contains error information if the boolean is False.
    '''

    if not valid_url_extension(url):
        return (False, "The file does not appear to have a valid file extension")
    elif not valid_url_mimetype(url):
        return (False, "The URL's header's mimetype is not 'image'.")
    elif not image_exists(url):
        return (False, "The image does not appear to exist on the server.")
    else:
        # looks like we have a winner!
        return (True, "")
# end isImage


# supporting methods for isImage()
# AMD: vets that the url appears to tpoint to a valid file type extension.
def valid_url_extension(url, extension_list=VALID_IMAGE_EXTENSIONS):
    # http://stackoverflow.com/a/10543969/396300
    return any([url.endswith(e) for e in extension_list])

# checks the mimetype metadata
def valid_url_mimetype(url, mimetype_list=VALID_IMAGE_MIMETYPES):
    # http://stackoverflow.com/a/10543969/396300
    mimetype, encoding = mimetypes.guess_type(url)

    if mimetype:
        return any([mimetype.startswith(m) for m in mimetype_list])
    else:
        return False

# verifies the file actually exists on the target server.
def image_exists(url): #domain, path):
    # http://stackoverflow.com/questions/2486145/python-check-if-url-to-jpg-exists

    #AMD: need to parse out domain and path.  https://docs.python.org/2/library/urlparse.html
    parsed_url = urlparse(url)
    domain,path = urlparse(url).netloc, urlparse(url).path
    print(domain)
    print(path)

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


# debugging
if __name__ == "__main__":
    bad_ext = "file.ico"
    malicious_ext = "file.exe"
    bad_mimetype = "http://entropymine.com/jason/testbed/mime/oct/file.png"  #TODO: this test fails
    file_dne = "http://pixabay.com/zzz.jpg"
    really_an_image = "http://www.aljazeera.com/mritems/assets/images/aj-logo-lg.png"
    test_set = [bad_ext,malicious_ext,bad_mimetype,file_dne,really_an_image]
    for test in test_set:
        print(isImage(test))