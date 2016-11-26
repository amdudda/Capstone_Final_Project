from django.shortcuts import render
from .models import *
# Create your views here.

def index(request):
    patterns = SourceImage.objects.all()
    # context = { 'patterns':'nothing to see here','mainimg':'2016-11-18-12-51_sunflowers-1719119_150.jpg'}
    context = { 'patterns':patterns }
    return render(request,'PatternGenerator/index.html',context)

def viewpatterns(request,pk):
    '''
    Handles an http request and accepts a primary key value
    :param request: http request
    :param pk: primary key of parent image extracted from the http request
    :return: render a web page listing all available patterns for a particular image
    '''
    w = SourceImage.objects.get(id=pk)
    w_patterns = PatternImage.objects.filter(source_id=w)
    context = {
        'parent_img': w,
        'pattern_set': w_patterns
        }
    return render(request,'PatternGenerator/ViewPattern.html',context)

def showpattern(request,pk):
    '''
    Handles an http request to display a specific pattern
    :param request: http request info
    :param pk: primary key used to identify the corresponding bitmap and generate its pattern
    :return: render a web page with information about the pattern being requested
    '''
    from PIL import Image
    from .ImageTools import MakePattern
    import os
    # grab the pattern to be used for the image
    p = PatternImage.objects.get(id=pk)

    # then extract the rest of our data for the page based on the image's filename
    # fname = os.path.join('static','images','bitmaps',p.filename)
    # my_bmp = Image.open(fname)
    context = MakePattern.get_image_data(p.filename)

    # and also append our pattern object to the data so we can get some info frm that, too...
    context['pattern'] = p

    # finally, render the page with all that data!
    return render(request,'PatternGenerator/ShowPattern.html',context)