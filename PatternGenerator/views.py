from django.shortcuts import render
from .models import *
# Create your views here.

def index(request):
    patterns = SourceImage.objects.all()
    # context = { 'patterns':'nothing to see here','mainimg':'2016-11-18-12-51_sunflowers-1719119_150.jpg'}
    context = { 'patterns':patterns }
    return render(request,'PatternGenerator/index.html',context)

def viewpatterns(request):
    # need to get patterns for requested image
    # TODO for now we're not fussing with extracting selected image, just prove we can pass data to this view.
    w = SourceImage.objects.get(id=1)
    w_patterns = PatternImage.objects.filter(source_id=w)
    context = {
        'pattern_id': w.id,
        'pattern_set': w_patterns
        }
    return render(request,'PatternGenerator/ViewPattern.html',context)
