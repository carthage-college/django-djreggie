#Include these below
from django import forms
from django.core import validators #Need this for validation

from djreggie.changemajor.models import ChangeModel

class ChangeForm(forms.ModelForm):
 #Overrides this function so I can add custom validation
    def __init__(self, *args, **kwargs):
        super(ChangeForm, self).__init__(*args,**kwargs)
    
    def clean_student_id(self):
        data = self.cleaned_data['student_id']
        if not re.match(r'^(\d{5,7})$', data):
            raise forms.ValidationError('Must be 5-7 digits long')
        return data
    
    def clean_name(self):
        data = self.cleaned_data['name']
        if not re.match(r'^((?:[a-zA-Z]+\s?){1,2}[a-zA-Z]+)$', data):
            raise forms.ValidationError('Please enter a valid name')
        return data
    
    def clean_advisor(self):
        data = self.cleaned_data['advisor']
        if not re.match(r'^((?:[a-zA-Z]+\s?){1,2}[a-zA-Z]+)$', data):
            raise forms.ValidationError('Please enter a valid advisor name')
        return data

    #Global options    
    class Meta:
        model = ChangeModel