#Include django.forms
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
import re

#I need the form
from djreggie.consentform.models import Form
        
# Create your forms here.
class ModelForm(forms.ModelForm):
    
    #This is needed if you want to add error messages, labels or additional validation for fields
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        
    #def clean_name(self):
    #    data = self.cleaned_data['name']
    #    if not re.match(r'^((?:[a-zA-Z]+\s?){1,2}[a-zA-Z]+)$', data):
    #        raise forms.ValidationError('Invalid name')
    #    return data
    
    def clean_student_ID(self):
        data = self.cleaned_data['student_ID']
        if not re.match(r'^(\d{5,7})$', data):
            raise forms.ValidationError('Must be 5-7 digits long')
        return data
    
    CHOICES = (
        ("CONSENT", 'I authorize and consent to the release of my directory information'),
        ("NOCONSENT", 'I hereby request that Carthage College not release my directory information.'),
    )
    
    #adding the validators field at the end here lets us use that function at the top to validate
    consent = forms.ChoiceField(widget = forms.RadioSelect, choices = CHOICES) 
    
    #Global options    
    class Meta:
        model = Form #The fields from the model 'Form' will be the same fields in this form
