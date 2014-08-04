#Include django.forms
from django import forms
from django.db import models
from django.core import validators #Need this to have custom validation in this file
from django.core.exceptions import ValidationError #Used for 'must_be_true' method
import re

#Also be sure to include the model
from djreggie.undergradcandidacy.models import UndergradModel
        
#My class with all of my fields are in here        
class UndergradForm(forms.ModelForm):
    
    #This is needed if you want to add error messages, labels or additional validation for fields
    def __init__(self, *args, **kwargs):
        super(UndergradForm, self).__init__(*args, **kwargs)
        self.fields["will_teach"].choices = self.fields["will_teach"].choices[1:]
        
    def clean_fname(self):
        data = self.cleaned_data['fname']
        if not re.match(r'^([a-zA-Z]+)$', data):
            raise forms.ValidationError('Please enter just a first name.')
        return data    
    def clean_mname(self):
        data = self.cleaned_data['mname']
        if data and not re.match(r'^([a-zA-Z]+|[a-zA-Z]\.?)$', data):
            raise forms.ValidationError('Please enter just a middle name or initial.')
        return data    
    def clean_lname(self):
        data = self.cleaned_data['lname']
        if not re.match(r'^([a-zA-Z]+)$', data):
            raise forms.ValidationError('Please enter just a last name.')
        return data
    
    def clean_best_phone(self):
        data = self.cleaned_data['best_phone']
        if not re.match(r'^(\d{4}|\d{3}[\s\-\.]?\d{4}|1?[\s\-\.]?\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4})$', data):
            raise forms.ValidationError('Enter a valid phone number')
        return data
    
    def clean_cell(self):
        data = self.cleaned_data['cell']
        if not re.match(r'^(\d{4}|\d{3}[\s\-\.]?\d{4}|1?[\s\-\.]?\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4})$', data):
            raise forms.ValidationError('Enter a valid phone number')
        return data
    
    def clean_state(self):
        data = self.cleaned_data['state']
        if not re.match(r'^((?:[a-zA-Z]+\s?)+[a-zA-Z]+)$', data):
            raise forms.ValidationError('Invalid state')
        return data
    
    def clean_zipcode(self):
        data = self.cleaned_data['zipcode']
        if not re.match(r'^([\d]{5}|\d{5}-?\d{4})$', str(data)):
            raise forms.ValidationError('Enter a valid zipcode')
        return data
    
    def clean_student_id(self):
        data = self.cleaned_data['student_id']
        if not re.match(r'^(\d{5,7})$', str(data)):
            raise forms.ValidationError('Not a valid 5-7 digit Carthage id')
        return data
    
    
    #Global options for the form    
    class Meta:
        model = UndergradModel #Use all of the fields from 'UndergradForm' in this form class
        widgets = { #When we want things displayed differently than their default
            'student_id': forms.HiddenInput(),
            'will_teach': forms.RadioSelect(),
        }