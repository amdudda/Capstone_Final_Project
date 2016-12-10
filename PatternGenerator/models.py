from __future__ import unicode_literals

from django.db import models

# Create your models here.

class SourceImage(models.Model):
    # this stores data bout the source image
    filename = models.CharField("file name",max_length=200)
    width = models.DecimalField("image width in inches",decimal_places=2,max_digits=6)
    height = models.DecimalField("image height in inches",decimal_places=2,max_digits=6)
    saved = models.DateTimeField("saved date",auto_now_add=True) # auto_now_add sets value to creation time

    def __str__(self):
        return "Image #%d, filename: %s, saved: %s" % (self.id,self.filename, str(self.saved))

class PatternImage(models.Model):
    # patterns can be reconstructed directly from bitmaps... color info, rgb info, all is stored there natively and
    # would be redundant in the database other than to speed up retrieval.  But some stuff I do want to store so I
    # don't have to brute-force calculate them every time I load an image!
    filename = models.CharField("file name", max_length=200,unique=True)
    created = models.DateTimeField("creation date", auto_now_add=True)  # auto_now_add sets value to creation time
    spi = models.IntegerField("stitches per inch",default=10)
    rpi = models.IntegerField("rows per inch",default=10)
    colors = models.IntegerField("colors in pattern",default=16)
    source_id = models.ForeignKey(SourceImage) # links to source image http://stackoverflow.com/questions/14663523/foreign-key-django-model#14663580

    def __str__(self):
        return "Pattern #%d, filename: %s, created: %s" % (self.id,self.filename,str(self.created))

class ImageTags(models.Model):
    # this allows multiple tags to be associated with an image.
    # it's SUPER annoying that Django doesn't support multicolumn PKs... :(
    source_img = models.ForeignKey(SourceImage) # links to the source image
    tag = models.CharField("tag",max_length=25) # I'm going to limit tags to 25 characters so they're short-ish

    def __str__(self):
        return self.source_img.filename + ": " + self.tag

    def _img_save_date(self):
        return self.source_img.saved
    img_save_date = property('source_img.saved')

    # class Meta:
    #     ordering = ['img_save_date']
