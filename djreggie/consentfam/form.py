#Include django.forms
from django import forms
from djreggie.consentfam.models import ConsentModel, ParentForm  #Include the models that goes with this form

#These carry special tools useful for validating django forms
from django.core.exceptions import ValidationError
from django.core import validators
import re
from djzbar import settings
from djreggie import settings
from djzbar.utils.informix import do_sql
from sqlalchemy import create_engine

# Create your forms here.
class ModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

    #clean functions are our validation functions
    def clean_student_id(self):
        data = self.cleaned_data['student_id'] #This is how we get the field we want to validate
        if not re.match(r'^(\d{5,7})$', data): #This checks the data against a regex function
            raise forms.ValidationError('Must be 5-7 digits long') #This is what will be displayed if there is an error in the code.
        return data

    class Meta:
        model = ConsentModel


class Parent(forms.Form):
    #Create fields here instead of in models so we can use a formset 
    form = forms.IntegerField(widget=forms.HiddenInput(), required=False) #this is the foreign key
    SHARE_AREA = ( #this sets up our choices when it comes to what we'd like to share
        ("ACADEMIC", 'Academic Records'),
        ("FINANCIAL", 'Financial Records'),
        ("BOTH", 'I would like to share both'),
        ("NEITHER", 'I would like to share neither'),
    )
    share = forms.ChoiceField(choices=SHARE_AREA) #this is the field that uses the choices above
    name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=16)
    email = forms.EmailField()
    RELATIVE = (    #more choices for another field
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
    relation = forms.ChoiceField(choices=RELATIVE,
                                widget=forms.RadioSelect(), #We've given this field a widget that will change its appearance on the page
                                label='Relation')

    def save(self): #This is how we "save" data to the database
        #put data in staging tables
        #see if entry for this contact already exists in database. if so update instead of add new one
        ferpaCountSQL = '''SELECT COUNT(ferpafamilyrec_no) AS cnt
                FROM cc_stg_ferpafamily_rec
                WHERE ferpafamily_no = %(form)d
                AND name = "%(name)s"
                AND relation = "%(relation)s"''' % (self.cleaned_data)
        entry = do_sql(ferpaCountSQL, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL).first()['cnt']
        if entry:
            updateFerpaSQL = '''UPDATE cc_stg_ferpafamily_rec
                    SET phone = "%(phone)s",
                        email = "%(email)s",
                        allow = "%(share)s"
                    WHERE ferpafamily_no = %(form)d
                    AND name = "%(name)s"
                    AND relation = "%(relation)s"''' % (self.cleaned_data)
            do_sql(updateFerpaSQL, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)
        else:
            insertFerpaSQL = '''INSERT INTO cc_stg_ferpafamily_rec (ferpafamily_no, name, relation, phone, email, allow)
                    VALUES (%(form)d, "%(name)s", "%(relation)s", "%(phone)s", "%(email)s", "%(share)s")''' % (self.cleaned_data)
            do_sql(insertFerpaSQL, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)