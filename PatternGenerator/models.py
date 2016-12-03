from __future__ import unicode_literals

from django.db import models

# Create your models here.

class SourceImage(models.Model):
    # this stores data bout the source image
    filename = models.CharField("file name",max_length=200)
    width = models.IntegerField("image width in pixels",default=0)
    height = models.IntegerField("image height in pixels",default=0)
    saved = models.DateTimeField("saved date",auto_now_add=True) # auto_now_add sets value to creation time

    def __str__(self):
        return "Image filename: " + self.filename + ", last saved: " + str(self.saved)

class PatternImage(models.Model):
    # TODO: what do I actually want to store about the bitmaps?
    # patterns can be reconstructed directly from bitmaps... color info, rgb info, all is stored there natively and
    # would be redundant in the database other than to speed up retrieval.
    filename = models.CharField("file name", max_length=200)
    created = models.DateTimeField("creation date", auto_now_add=True)  # auto_now_add sets value to creation time
    spi = models.IntegerField("stitches per inch",default=10)
    rpi = models.IntegerField("rows per inch",default=10)
    colors = models.IntegerField("colors in pattern",default=16)
    source_id = models.ForeignKey(SourceImage) # links to source image http://stackoverflow.com/questions/14663523/foreign-key-django-model#14663580

    def __str__(self):
        return self.filename
