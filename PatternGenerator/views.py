from django.shortcuts import render
from .models import *
# Create your views here.

def index(request):
    context = { 'patterns':'nothing to see here','mainimg':'2016-11-18-12-51_sunflowers-1719119_150.jpg'}
    return render(request,'PatternGenerator/index.html',context)