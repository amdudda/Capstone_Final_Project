from .ImageTools.ImageValidator import isImage
from django.utils.translation import ugettext as _
from django import forms


class UploadURLForm(forms.Form):
    url = forms.URLField(required=True,
        error_messages={
            "required": "Please enter a valid URL to an image (.bmp, .eps, .gif, .jpg, .jpeg, .png, .tiff)."
        }
    )

    def clean_url(self):
        url = self.cleaned_data['url'].lower()
        isImg, ErrMsg = isImage(url)
        if not isImg:
            raise forms.ValidationError(_(ErrMsg))
        return url
