#Include django.forms
from django import forms
from django.db import models
from django.core import validators #Need this to have custom validation in this file
from django.core.exceptions import ValidationError #Used for 'must_be_true' method
import re

#Also be sure to include the model
from djreggie.undergradcandidacy.models import UndergradForm

#A simple test
def must_be_true(value):
    if value == False:
        raise ValidationError('box must be checked')
        
#My class with all of my fields are in here        
class UndergradFormForm(forms.ModelForm):
    
    #This is needed if you want to add error messages, labels or additional validation for fields
    def __init__(self, *args, **kwargs):
        super(UndergradFormForm, self).__init__(*args, **kwargs)
        
        #Setting settings for select boxes
        self.fields['finish_requirements_by'].choices = self.fields['finish_requirements_by'].choices[1:]
        self.fields['when_teach'].choices = self.fields['when_teach'].choices[1:]
        
        #Custom validation for fields
        #self.fields['fname'].validators = [validators.RegexValidator(regex='^.+$', message='Enter a valid first name', code='bad_fname')]
        #self.fields['mname'].validators = [validators.RegexValidator(regex='^.+$', message='Enter a valid middle name', code='bad_mname')]
        #self.fields['lname'].validators = [validators.RegexValidator(regex='^.+$', message='Enter a valid last name', code='bad_lname')]
        #self.fields['email'].validators = [validators.RegexValidator(regex='^[A-Za-z0-9\.\_\%\+\-]+@[A-Za-z0-9\.\-]+\.[A-Za-z]{2,4}$', message='Enter a valid email', code='bad_email')]
        #self.fields['best_phone'].validators = [validators.RegexValidator(regex='^(\d{4}|\d{3}[\s\-\.]?\d{4}|1?[\s\-\.]?\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4})$', message='Enter a valid phone number', code='bad_phone')]
        #self.fields['cell'].validators = [validators.RegexValidator(regex='^(\d{4}|\d{3}[\s\-\.]?\d{4}|1?[\s\-\.]?\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4})$', message='Enter a valid phone number', code='bad_phone')]
        #self.fields['state'].validators = [validators.RegexValidator(regex='^\w{2}$', message='Invalid state', code='bad_state')]
        #self.fields['zipcode'].validators = [validators.RegexValidator(regex='^\d{5}$', message='Enter a valid zipcode', code='bad_zip')]
        #self.fields['student_id'].validators = [validators.RegexValidator(regex=('^[\d]{5,7}$'),message='Not a valid 5-7 digit Carthage id',code='a')]
        
        #Custom labels for fields
        #self.fields['fname'].label = 'First Name'
        #self.fields['mname'].label = 'Middle Name'
        #self.fields['lname'].label = 'Last Name'
        #self.fields['cell'].label = 'Cell'
        #self.fields['best_phone'].label = 'Best phone'
        #self.fields['carthage_email'].label = 'Check if carthage email'
        #self.fields['email'].label = 'Email'
        #self.fields['zipcode'].label = 'Zip'
        
    def clean_fname(self):
        data = self.cleaned_data['fname']
        if not re.match(r'^([a-zA-Z]+)$', data):
            raise forms.ValidationError('Please enter just a first name.')
        return data    
    def clean_mname(self):
        data = self.cleaned_data['mname']
        if not re.match(r'^([a-zA-Z]+)$', data):
            raise forms.ValidationError('Please enter just a middle name.')
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
        if not re.match(r'^([\d]{5}|\d{5}-?\d{4})$', data):
            raise forms.ValidationError('Enter a valid zipcode')
        return data
    
    def clean_student_id(self):
        data = self.cleaned_data['student_id']
        if not re.match(r'^(\d{5,7})$', data):
            raise forms.ValidationError('Not a valid 5-7 digit Carthage id')
        return data
    
    
    #Global options for the form    
    class Meta:
        model = UndergradForm #Use all of the fields from 'UndergradForm' in this form class
        widgets = { #When we want things displayed differently than their default
            'finish_requirements_by': forms.RadioSelect(), #Radio select
            'when_teach': forms.RadioSelect(),
            'carthage_email': forms.HiddenInput(), #Is not visible
        }