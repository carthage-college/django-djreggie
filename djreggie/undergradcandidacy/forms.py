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
        #if not re.match(r'^([a-z]+)$', data, re.I):
        if not re.match(r'^(([a-z]+[\-\']?)*([a-z]+)?\s?)+\.?$', data, re.I):
            raise forms.ValidationError('Please enter just a first name.')
        return data    
    def clean_mname(self):
        data = self.cleaned_data['mname']
        #if data and not re.match(r'^([a-zA-Z]+|[a-zA-Z]\.?)$', data):
        if not re.match(r'^(([a-z]+[\-\']?)*([a-z]+)?\s?)+\.?$', data, re.I):
            raise forms.ValidationError('Please enter just a middle name or initial.')
        return data    
    def clean_lname(self):
        data = self.cleaned_data['lname']
        #if not re.match(r'^([a-zA-Z]+)$', data):
        if not re.match(r'^(([a-z]+[\-\']?)*([a-z]+)?\s?)+\.?$', data, re.I):
            raise forms.ValidationError('Please enter just a last name.')
        return data

    def clean_fnamepro(self):
        data = str(self.cleaned_data['fnamepro']).replace('"', '')
        return data
    def clean_mnamepro(self):
        data = str(self.cleaned_data['mnamepro']).replace('"', '')
        return data
    def clean_lnamepro(self):
        data = str(self.cleaned_data['lnamepro']).replace('"', '')
        return data
    
    def clean_state(self):
        data = self.cleaned_data['state']
        if data != None and not re.match(r'^((?:[a-zA-Z]+\s?)+[a-zA-Z]+)$', data):
            raise forms.ValidationError('Invalid state')
        return data
    
    def clean_zipcode(self):
        data = self.cleaned_data['zipcode']
        if data != None and not re.match(r'^([\d]{5}|\d{5}-?\d{4})$', str(data)):
            raise forms.ValidationError('Enter a valid zipcode')
        return data
    
    def clean_student_id(self):
        data = self.cleaned_data['student_id']
        if not re.match(r'^(\d{5,7})$', str(data)):
            raise forms.ValidationError('Not a valid 5-7 digit Carthage id')
        return data
    
    def clean(self):
        cleaned_data = super(UndergradForm, self).clean()
        if cleaned_data.get('will_teach') == 'Y': # if said yes to will teach have year_teach and term be required
            if not cleaned_data.get('year_teach'):
                self.errors['year_teach'] = self.error_class(['This field is required'])
            if not cleaned_data.get('term'):
                self.errors['term'] = self.error_class(['This field is required'])
                
        if cleaned_data.get('best_contact') == 'EML':
            if not re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', cleaned_data.get('best_contact_value')):
                self.errors['best_contact_value'] = self.error_class(['You must enter a valid email address'])
                del cleaned_data['best_contact_value']
        elif cleaned_data.get('best_contact') == 'PHN':
            if not re.match(r'^((?:1?[\s\-\.\/]?\(?(?:\d{3})\)?)?[\s\-\.\/]?\d{3}[\s\-\.\/]?\d{4}(?:\s?(?:x|ext|\.)?\s?\d{4})?)$',
                            cleaned_data.get('best_contact_value')):
                self._errors['best_contact_value'] = self.error_class(['You must enter a valid phone number'])
                del cleaned_data['best_contact_value']
        else:
            self.errors['best_contact'] = self.error_class(['This field is required'])
                
        return cleaned_data
    
    #Global options for the form    
    class Meta:
        model = UndergradModel #Use all of the fields from 'UndergradForm' in this form class
        widgets = { #When we want things displayed differently than their default
            'student_id': forms.HiddenInput(),
            'will_teach': forms.RadioSelect(),
        }