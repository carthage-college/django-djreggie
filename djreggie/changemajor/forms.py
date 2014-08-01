#Include these below
from django import forms
from django.core import validators #Need this for validation
import re
from djzbar.settings import INFORMIX_EARL_TEST
from sqlalchemy import create_engine

from djreggie.changemajor.models import ChangeModel

class ChangeForm(forms.ModelForm):
 #Overrides this function so I can add custom validation
    def __init__(self, *args, **kwargs):
        super(ChangeForm, self).__init__(*args,**kwargs)
    
    def clean_student_id(self):
        data = self.cleaned_data['student_id']
        if not re.match(r'^(\d{5,7})$', data):
            raise forms.ValidationError('Must be 5-7 digits long')
        return data
    
    def clean_name(self):
        data = self.cleaned_data['name']
        if not re.match(r'^((?:[a-zA-Z]+(?:\,?\s)?){1,2}[a-zA-Z]+\.?)$', data):
            raise forms.ValidationError('Please enter a valid name')
        return data
    
    def clean_advisor(self):
        data = self.cleaned_data['advisor']
        #make sure there is something in data so there wont be an error with the sql
        if data:
            engine = create_engine(INFORMIX_EARL_TEST)
            connection = engine.connect()
            #try to find advisor id in database to see if this id is for a valid advisor
            sql = '''SELECT COUNT(*) AS count
                    FROM job_rec
                    INNER JOIN id_rec ON job_rec.id = id_rec.id
                    WHERE hrstat = 'FT'
                    AND TODAY BETWEEN job_rec.beg_date AND NVL(job_rec.end_date, TODAY)
                    AND job_rec.id = %s''' % (data)
            advisor = connection.execute(sql)
            if not re.match(r'^(\d{5,7}|)$', data) or not advisor.first()['count']:
                raise forms.ValidationError('Please enter a valid advisor')
        return data

    #Global options    
    class Meta:
        model = ChangeModel