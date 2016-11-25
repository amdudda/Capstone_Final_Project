from django.contrib import admin

# Register your models here.

from .models import PatternImage, SourceImage

my_models = [SourceImage,PatternImage]
admin.site.register(my_models)
