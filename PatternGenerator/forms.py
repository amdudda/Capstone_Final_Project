from .ImageTools.ImageValidator import isImage
from django.utils.translation import ugettext as _
from django import forms

# borrows heavily from http://pythoncentral.io/how-to-use-python-django-forms/http://pythoncentral.io/how-to-use-python-django-forms/
class UploadURLForm(forms.Form):
    url = forms.URLField(required=True,
        error_messages={
            "required": "Please enter a valid URL to an image (.bmp, .eps, .gif, .jpg, .jpeg, .png, .tiff)."
        }
    )

    def is_clean(self):
        the_url = self.cleaned_data['url']
        isImg, ErrMsg = isImage(the_url)
        if not isImg:
            raise forms.ValidationError(_(ErrMsg))
        return isImg
    #
    # def clean_url(self):
    #     url = self.cleaned_data['url'].lower()
    #     print(url)
    #     isImg, ErrMsg = isImage(url)
    #     if not isImg:
    #         raise forms.ValidationError(_(ErrMsg))
    #     return url


# TODO set up a form for pattern generation to exploit built-in validation
class GeneratePatternForm(forms.Form):
    spi = forms.IntegerField(
        label="Stitches per Inch",
        initial=10,
        required=True,
        error_messages={"required":"Please enter an integer number of stitches per inch."}
    )
    rpi = forms.IntegerField(
        label="Rows Per Inch",
        initial=10,
        required=True,
        error_messages={"required":"Please enter an integer number of rows per inch."}
    )
    numcolors = forms.IntegerField(
        label="Number of Colors",
        initial=8,
        max_value=16,
        min_value=2
    )
