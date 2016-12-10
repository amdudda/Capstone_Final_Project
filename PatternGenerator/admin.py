from django.contrib import admin

# Register your models here.

from .models import *

my_models = [SourceImage,PatternImage,ImageTags]
admin.site.register(my_models)
