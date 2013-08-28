#Include these below
from django import forms
from django.core import validators #Need this for validation

from djreggie.changemajor.models import Student

#This is the model that includes all the fields that are in the form
class StudentForm(forms.ModelForm):

    #Overrides this function so I can add custom validation
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args,**kwargs)
        
        #I add validators for fields
        self.fields['student_id'].validators = [validators.RegexValidator(regex=(r'^\d{5,7}$'),message='Must be 5-7 digits long',code='a')]
        self.fields['name'].validators = [validators.RegexValidator(regex=('^[a-zA-Z\']+[a-zA-Z\-\s\']+$'),message='Please enter a valid name',code='a')]
        self.fields['advisor'].validators = [validators.RegexValidator(regex=('^[a-zA-Z\']+[a-zA-Z\-\s\']+$'),message='Please enter a valid advisor name',code='a')]
        
        #Error messages
        self.fields['student_id'].error_messages = {'required':'Enter a student id'}
        self.fields['name'].error_messages = {'required':'Enter a valid name'}

    #Global options    
    class Meta:
        model = Student    
    widgets = {
        'student_id': forms.TextInput(attrs={'maxlength':7})
    }
