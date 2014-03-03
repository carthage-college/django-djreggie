#Include django.forms
from django import forms
from djreggie.consentfam.models import ConsentModel, ParentForm, Contact  #Include the models that goes with this form

#These carry special tools useful for validating django forms
from django.core.exceptions import ValidationError
from django.core import validators

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
        
        self.fields['Carthage_ID_Number'].label = 'Student ID'
        self.fields['Full_Name_of_Student'].label = 'Name'
        
        #self.fields['Full_Name_of_Student'].validators = [validators.RegexValidator(regex=('^[a-zA-Z\']+[a-zA-Z\-\s\']+$'), message='Invalid name', code='bad_name')]
        self.fields['Carthage_ID_Number'].validators = [validators.RegexValidator(regex=('^\d{5,7}$'), message='Must be 5-7 digits long', code='bad_id')]
        self.fields['Which_information_would_you_like_to_share'].validators = [notnull]

    class Meta:
        model = ConsentModel
        exclude = ('name', 'Relation',)
        #widgets = {
        #    'Carthage_ID_Number': forms.HiddenInput(),
        #    'Full_Name_of_Student': forms.HiddenInput(),
        #}

class Parent(forms.Form):
    name = forms.CharField()
    
    CHOICES3 = (    
    ("wrong", '-------'),
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
    Relation = forms.ChoiceField(required = False, widget = forms.Select, choices = CHOICES3, validators = [fff]) 
