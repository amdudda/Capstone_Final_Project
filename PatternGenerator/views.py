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
