from __future__ import unicode_literals

from django.db import models

# Create your models here.

class SourceImage(models.Model):
    # this stores data bout the source image
    filename = models.CharField("file name",max_length=200)
    saved = models.DateTimeField("saved date",auto_now_add=True) # auto_now_add sets value to creation time

class PatternImage(models.Model):
    # TODO: what do I actually want to store about the bitmaps?
    # patterns can be reconstructed directly from bitmaps... color info, rgb info, all is stored there natively and
    # would be redundant in the database other than to speed up retrieval.
    filename = models.CharField("file name", max_length=200)
    created = models.DateTimeField("creation date", auto_now_add=True)  # auto_now_add sets value to creation time
    spi = models.IntegerField("stitches per inch")
    rpi = models.IntegerField("rows per inch")
    source_id = models.ForeignKey(SourceImage) # links to source image http://stackoverflow.com/questions/14663523/foreign-key-django-model#14663580