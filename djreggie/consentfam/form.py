#Include django.forms
from django import forms
from djreggie.consentfam.models import ConsentModel, ParentForm, Contact  #Include the models that goes with this form

#These carry special tools useful for validating django forms
from django.core.exceptions import ValidationError
from django.core import validators
import re

#Validation for the 'relation' field
def fff (value):
    if value == "wrong":
        raise ValidationError(message = 'Must choose a relation', code="a")
        
def notnull (value):
    if value == None:
        raise ValidationError(message = 'Must choose an option', code='a')
        
# Create your forms here.
class ModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        
    def clean_Full_Name_of_Student(self):
        data = self.cleaned_data['Full_Name_of_Student']
        if not re.match(r'^((?:[a-zA-Z]+\s?){1,2}[a-zA-Z]+)$', data):
            raise forms.ValidationError('Invalid name')
        return data
    
    def clean_Carthage_ID_Number(self):
        data = self.cleaned_data['Carthage_ID_Number']
        if not re.match(r'^(\d{5,7})$', data):
            raise forms.ValidationError('Must be 5-7 digits long')
        return data
    
    def clean_Which_information_would_you_like_to_share(self):
        data = self.cleaned_data['Which_information_would_you_like_to_share']
        if not data:
            raise forms.ValidationError('Must choose an option')
        return data
    
    
    class Meta:
        model = ConsentModel
        exclude = ('name', 'Relation',)


class Parent(forms.Form):
    name = forms.CharField()
    
    CHOICES3 = (    
    ("MOM", 'Mother'),
    ("DAD", 'Father'),
    ("GRAN", 'Grandparent'),
    ("BRO", 'Brother'),
    ("SIS", 'Sister'),
    ("AUNT", 'Aunt'),
    ("UNC", 'Uncle'),
    ("HUSB", 'Husband'),
    ("FRIE", 'Friend'),
    ("OTHE", 'Other'),
    ("STEP", 'Stepparent'),
    )
    
    #adding the validators field at the end here lets us use that function at the top to validate
    Relation = forms.ChoiceField(required = False, widget = forms.RadioSelect, choices = CHOICES3, validators = [fff]) 
