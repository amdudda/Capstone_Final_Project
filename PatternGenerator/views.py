from django.shortcuts import render
from .models import *
# Create your views here.

def index(request):
    context = { 'patterns':'nothing to see here',}
    return render(request,'PatternGenerator/index.html',context)