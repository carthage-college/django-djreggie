#Include django.forms
from django import forms
from djreggie.consentfam.models import ConsentModel, ParentForm  #Include the models that goes with this form

#These carry special tools useful for validating django forms
from django.core.exceptions import ValidationError
from django.core import validators
import re
from djzbar.settings import INFORMIX_EARL_TEST
from sqlalchemy import create_engine

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
            
    def clean_student_id(self):
        data = self.cleaned_data['student_id']
        if not re.match(r'^(\d{5,7})$', data):
            raise forms.ValidationError('Must be 5-7 digits long')
        return data
    
    def clean_phone(self):
        data = self.cleaned_data['phone']
        if not re.match(r'^((?:1?[\s\-\.\/]?\(?(?:\d{3})\)?)?[\s\-\.\/]?\d{3}[\s\-\.\/]?\d{4}(?:\s?(?:x|ext|\.)?\s?\d{4})?)$', data):
            raise forms.ValidationError('Please enter a valid phone number')
        return data
    
    
    class Meta:
        model = ConsentModel


class Parent(forms.Form):
    #have to create fields here instead of in models so we can use a formset
    form = forms.IntegerField(widget=forms.HiddenInput(),required=False)
    CHOICES = (
        ("ACADEMIC", 'Academic Records'),
        ("FINANCIAL", 'Financial Records'),
        ("BOTH", 'I would like to share both'),
        ("NEITHER", 'I would like to share neither'),
    )
    share = forms.ChoiceField(choices=CHOICES)    
    name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=16)
    email = forms.EmailField()
    CHOICES2 = (    
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
    relation = forms.ChoiceField(choices=CHOICES2,
                                widget=forms.RadioSelect(),
                                label='Relation')
    
    def save(self):
        engine = create_engine(INFORMIX_EARL_TEST)
        connection = engine.connect()
        #put data in staging tables
        sql = '''INSERT INTO cc_stg_ferpafamily_rec (ferpafamily_no, name, relation, phone, email, allow)
                VALUES (%(form)d, "%(name)s", "%(relation)s", "%(phone)s", "%(email)s", "%(share)s")''' % (self.cleaned_data)
        connection.execute(sql)