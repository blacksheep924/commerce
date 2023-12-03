from django import forms

class Newitem(forms.Form):
    item = forms.CharField(label='Your item', max_length = 100)
    startbid = forms.FloatField(label='Start bid')
    image = forms.URLField(label='Image URL')
    description = forms.CharField(widget=forms.Textarea)