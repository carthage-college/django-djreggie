#Include these below
from django import forms
from django.core import validators #Need this for validation
import re
from djzbar import settings
from djreggie import settings
from sqlalchemy import create_engine
from djzbar.utils.informix import do_sql
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
        #Find updated regex that allows for an apostrophe in the name
        if not re.match(r'^((?:[a-zA-Z]+(?:\,?\s)?){1,2}[a-zA-Z]+\.?)$', data):
            raise forms.ValidationError('Please enter a valid name')
        return data

    def clean_advisor(self):
        data = self.cleaned_data['advisor']
        #make sure there is something in data so there wont be an error with the sql
        advisor_name = data.split(', ')
        if len(advisor_name) == 2:
            #try to find advisor id in database to see if this id is for a valid advisor
            sql = '''SELECT job_rec.id AS id
                    FROM job_rec
                    INNER JOIN id_rec ON job_rec.id = id_rec.id
                    WHERE hrstat = 'FT'
                    AND TODAY BETWEEN job_rec.beg_date AND NVL(job_rec.end_date, TODAY)
                    AND id_rec.firstname = "%s"
                    AND id_rec.lastname = "%s"''' % (advisor_name[1], advisor_name[0])
            result = do_sql(sql, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)
            advisor = result.first()
            if not advisor:
                raise forms.ValidationError('Please enter a valid advisor')
            else:
                return advisor['id']
        elif data != '':
            raise forms.ValidationError('Please enter a valid advisor')
        return data

    #Global options
    class Meta:
        model = ChangeModel
        fields = '__all__'
