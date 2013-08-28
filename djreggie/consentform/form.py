#Include django.forms
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

#I need the form
from djreggie.consentform.models import Form
        
# Create your forms here.
class ModelForm(forms.ModelForm):
    
    #This is needed if you want to add error messages, labels or additional validation for fields
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        
        #I am adding validation here
        self.fields['name'].validators = [validators.RegexValidator(regex=('^[a-zA-Z\']+[a-zA-Z\-\s\']+$'), message='Invalid name', code='invalid_name')]
        self.fields['student_ID'].validators = [validators.RegexValidator(regex=('^\\d{5,7}$'), message='Must be 5-7 digits long', code='bad_id')]
    
    #Global options    
    class Meta:
        model = Form #The fields from the model 'Form' will be the same fields in this form
        widgets = { #If we want to change the display of fields
            'student_ID': forms.TextInput(attrs={'maxlength':7})
        }
        
