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
