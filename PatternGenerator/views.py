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
    return render(request,'PatternGenerator/ViewPatterns.html',context)

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
    context = MakePattern.get_image_data(p.filename)

    # and also append our pattern object to the data so we can get some info from that, too...
    context['pattern'] = p

    # finally, render the page with all that data!
    return render(request,'PatternGenerator/ShowPattern.html',context)

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
        context = {'src_img' : SourceImage.objects.get(id=pk)}

        # then render the page
        return render(request,'PatternGenerator/GeneratePattern.html',context)

    # POST means they want to generate a pattern
    if request.method == "POST":
        r_data = request.POST
        print(r_data)
        rpi = r_data['rpi']
        spi = r_data['spi']
        num_colors = r_data['numcolors']

        print('rpi %s'% rpi)
        context = {'src_img': SourceImage.objects.get(id=pk)}

        # till I figure out what the form data looks like, just go back to the generation page
        return render(request,'PatternGenerator/GeneratePattern.html',context)