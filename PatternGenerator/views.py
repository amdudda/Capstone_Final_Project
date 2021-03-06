from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *
from .ImageTools import MakePattern, ImageValidator, ImageDownloader
from .forms import UploadURLForm,GeneratePatternForm
from os import path
import time

# Global variable for website name so I can change it easily later
WEBSITE_NAME = "Patternmaker's Guild"

# Create your views here.

def index(request):
    '''
    Returns the main page of the site
    :param request: the originating URL request
    :return: the index page of the site
    '''
    patterns = SourceImage.objects.all().order_by("-saved")
    context = {
        'patterns':patterns,
        'title': "%s Pattern Database" % WEBSITE_NAME,
        'subhead':"Pattern Database"
    }
    return render(request,'PatternGenerator/index.html',context)

def viewpatterns(request,pk):
    '''
    Handles an http request and accepts a primary key value
    :param request: http request
    :param pk: primary key of parent image extracted from the http request
    :return: render a web page listing all available patterns for a particular image
    '''
    w = SourceImage.objects.get(id=pk)
    w_patterns = PatternImage.objects.filter(source_id=w).order_by("-created")
    context = {
        'parent_img': w,
        'pattern_set': w_patterns,
        'title': "%s Patterns" % WEBSITE_NAME,
        'subhead': "Pattern Set %s" % pk,
        }
    return render(request,'PatternGenerator/ViewPatterns.html',context)
# end viewpatterns

def showpattern(request,pk):
    '''
    Handles an http request to display a specific pattern
    :param request: http request info
    :param pk: primary key used to identify the corresponding bitmap and generate its pattern
    :return: render a web page with information about the pattern being requested
    '''
    # grab the pattern to be used for the image
    p = PatternImage.objects.get(id=pk)

    # then extract the rest of our data for the page based on the image's filename
    context = MakePattern.get_image_data(p.filename)

    # and also append our pattern object to the data so we can get some info from that, too...
    context['pattern'] = p
    context['title'] = "%s Pattern #%s"% (WEBSITE_NAME,pk)
    context['subhead'] = 'Pattern ID Number %s' % pk

    # finally, render the page with all that data!
    return render(request,'PatternGenerator/ShowPattern.html',context)
# end showpattern

def genpattern(request,pk):
    '''
    This will pass a particular image that a user wants to use to create a pattern.
    :param request: the url request
    :param pk: the primary key identifying a particular source image
    :return: render a web page that will let people generate patterns
    '''

    # GET means they want to fetch an image to work with
    if request.method == "GET":
        # grab the image and put it in the context variable
        context = {
            'src_img' : SourceImage.objects.get(id=pk),
            'title': "%s Pattern Generator" % WEBSITE_NAME,
            'subhead' : "Generate a New Pattern!",
            'form' : GeneratePatternForm(),
        }

        # then render the page
        return render(request,'PatternGenerator/GeneratePattern.html',context)

    # POST means they want to generate a pattern - but let's make sure they've at least PRETENDED to pass a middleware token.
    if request.method == "POST" and request.POST['csrfmiddlewaretoken']:
        r_data = request.POST
        print(r_data)
        rpi = int(r_data['rpi'])
        spi = int(r_data['spi'])
        num_colors = int(r_data['numcolors'])

        '''
        Here we generate the bitmap, save it, and store the metadata in the database.
        Pass our settings to our image processor in ImageTools and let it handle the info for us...
        '''
        # first get the filepath of the source image
        src_img = SourceImage.objects.get(id=pk)
        new_pattern = create_new_pattern(src_img, num_colors, rpi, spi)

        # pass data relevant to the ShowPattern page.
        context = { 'pattern': new_pattern }

        # let's send the user to the new pattern after a wait of a couple of seconds to give the system a moment
        # to save the image
        time.sleep(4)
        # return render(request,'PatternGenerator/ShowPattern.html',context)
        url = "/ShowPattern/" + str(new_pattern.id)
        return HttpResponseRedirect(url)

# end genpattern

def create_new_pattern(src_img, num_colors=16, rpi=10, spi=10):

    src_fname = src_img.filename
    src_fpath = path.join("PatternGenerator", "static", "images", "source", src_fname)
    # generate file name & path for the bitmap, generate the bitmap, and save it.
    period = src_fname.rfind(".")
    src_name = src_fname[:period]
    target_fname = "%s_%sx%sx%s%s" % (src_name, spi, rpi, num_colors, ".bmp")
    target_fpath = path.join("PatternGenerator", "static", "images", "bitmaps", target_fname)

    # Disallow creation of duplicate records in db - check that the pattern doesn't already exist.  Pattern filenames should be unique, so let's just go with that.  Desired behavior would be to just return the already-existing image...
    # if the pattern already exists, return that, otherwise create it.
    try:
        # first record, Just In Case duplicates somehow have happened...
        new_pattern = PatternImage.objects.get(filename=target_fname)
    except:
        new_bmp = MakePattern.image2bitmap(src_fpath, spi=spi, rpi=rpi, farben=num_colors)
        new_bmp.save(target_fpath)

        while True:
            # check if the file is done writing - don't let code proceed until filewrite is done.
            try:
                # try a quick open-close of the file - there will be an IOError if file still being written
                file = open(target_fpath)
                file.close()
                break
            except:
                print('file still writing')
                # pass

        # and create the new record in the database
        new_pattern = PatternImage.objects.create(
            filename=target_fname,
            spi=spi,
            rpi=rpi,
            colors=num_colors,
            source_id=src_img
        )
    finally:
        return new_pattern
# end create_new_pattern


def upload_image(request):
    # modeled on example at http://pythoncentral.io/how-to-use-python-django-forms/
    if request.method == "GET":
        context= {
            'form' : UploadURLForm(),
            'title': "%s Image Uploader" % WEBSITE_NAME,
            'subhead': "Image Uploader" }
    else:
        # A POST request: Handle Form Upload
        form = UploadURLForm(request.POST)  # Bind data from request.POST to the form's one field
        context = { 'form': form , 'errmsg' : "err, what?"}
        # If form is valid, start doing data validation
        if form.is_valid():
            url = form.cleaned_data['url']
            # validate that the URL is an image:
            isImg, ErrMsg = ImageValidator.isImage(url)
            if not isImg:
                # oops, bad data, tell the user
                context = { 'form': form, 'errmsg' : ErrMsg}
            else:
                # yay, we seem to have valid data, let's download the image and save it to our database!
                source_img_filepath = path.join("PatternGenerator","static","images","source")
                saved_image = ImageDownloader.FetchImage(url,source_img_filepath)
                time.sleep(4) # wait for image file to finish writing
                if saved_image:
                    # yay we successfully saved the image and got a tuple of data back.
                    # save the image data to the database!
                    new_img = SourceImage.objects.create(
                        filename=saved_image[0],
                        width=saved_image[1],
                        height=saved_image[2]
                    )

                    # next, we create the default 10x10 "inch", 16 color bitmap for the image
                    new_pattern = create_new_pattern(src_img=new_img)

                    # then redirect the user to view the new image and its default pattern
                    redirect_url = "/ViewPatterns/" + str(new_img.id)
                    return HttpResponseRedirect('/')
                else:
                    # OOOOOOPS - we failed to download and save after all those checks.  Tell the user that.
                    context = {
                        'form': form,
                        'errmsg' : "We were unable to save the image.  No additional error information is available at this time."}
                    return render(request, 'PatternGenerator/UploadImage.html', context)
                # end if saved_image
            # end if not isImg
        elif (form.errors):
            # if you try to pass 'http://blarg.mp3' it returns an array of errors not dealt with above; let's cope with them here...  it's not the prettiest, but it at least tells the user *something* went wrong!
            if form.errors['url']:
                # concatenate the url-related errors into a string and add it to the context dictionary
                errstring = "; ".join(form.errors['url'])
                context['errmsg'] = errstring
            else:
                context['errmsg'] = "The following error(s) occurred:" + str(form.errors)
        # end if form.is_valid
    return render(request, 'PatternGenerator/UploadImage.html', context)
# end upload_image

def about(request):
    context = {
        'title': "%s Pattern Database" % WEBSITE_NAME,
        'subhead':"A Knack for the Needles"}
    return render(request,'PatternGenerator/about.html',context)

def show_by_tag(request,tag):
    # takes a tag and shows images associated with that tag
    my_images = ImageTags.objects.filter(tag=tag)
    my_images.order_by("-img_save_date")
    images = []
    for image in my_images:
        images.append(image.source_img)

    context = {
        'title': "%s Pattern Database" % WEBSITE_NAME,
        'subhead': "Images tagged with '%s'" % tag,
        'patterns': images
    }

    return render(request,'PatternGenerator/index.html',context)