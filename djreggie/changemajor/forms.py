#Include these below
from django import forms
from django.core import validators #Need this for validation

from djreggie.changemajor.models import Student
from djzbar.settings import INFORMIX_EARL_TEST
from sqlalchemy import create_engine


#SQL Alchemy
engine = create_engine(INFORMIX_EARL_TEST)
connection = engine.connect()

#Majors
sql1 = "select txt, major from major_table WHERE sysdate BETWEEN active_date AND NVL(inactive_date, sysdate) AND LENGTH(txt) > 0 AND web_display = 'Y' ORDER BY txt ASC"
major = connection.execute(sql1)
array1 = []
for row in major:
    array1.append((row['major'],row['txt']))   
CHOICES1 = tuple(array1)

#Minors
sql2 = "select txt, minor from minor_table WHERE sysdate BETWEEN active_date AND NVL(inactive_date, sysdate) AND LENGTH(txt) > 0 AND web_display = 'Y' ORDER BY txt ASC"
minor = connection.execute(sql2)
array2 = []
for row in minor:
    array2.append((row['minor'],row['txt']))   
CHOICES2 = tuple(array2)
connection.close()
#This is the model that includes all the fields that are in the form
class StudentForm(forms.ModelForm):

    #Overrides this function so I can add custom validation
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args,**kwargs)
        
        #I add validators for fields
        self.fields['student_id'].validators = [validators.RegexValidator(regex=(r'^\d{5,7}$'),message='Must be 5-7 digits long',code='a')]
        self.fields['name'].validators = [validators.RegexValidator(regex=('^[a-zA-Z\']+[a-zA-Z\-\s\']+$'),message='Please enter a valid name',code='a')]
        self.fields['advisor'].validators = [validators.RegexValidator(regex=('^[a-zA-Z\']+[a-zA-Z\-\s\']+$'),message='Please enter a valid advisor name',code='a')]
        self.fields['student_id'].label = 'Student ID'
        
        #Error messages
        self.fields['student_id'].error_messages = {'required':'Enter a student id'}
        self.fields['name'].error_messages = {'required':'Enter a valid name'}

    #Global options    
    class Meta:
        model = Student  
        exclude = ['majors', 'minors']
        widgets = {
            'student_id': forms.TextInput(attrs={'maxlength':7}),
        }


class MajorMinorForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super(MajorMinorForm, self).__init__(*args, **kwargs)
        
    majors_list = forms.CharField(widget=forms.SelectMultiple(choices=CHOICES1, attrs={'size': 5}), required=False)
    minors_list = forms.CharField(widget=forms.SelectMultiple(choices=CHOICES2, attrs={'size': 5}), required=False)
    majors = forms.CharField(widget=forms.SelectMultiple(attrs={'size':5}))
    minors = forms.CharField(widget=forms.SelectMultiple(attrs={'size':5}), required=False)
    
#test comment
