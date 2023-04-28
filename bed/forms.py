from django import forms


class UploadFileForm(forms.Form):
    file = forms.ImageField(max_length=10*1204*1024)
