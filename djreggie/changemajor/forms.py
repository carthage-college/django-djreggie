from django import forms
from django.conf import settings
from django.core import validators

from djreggie.changemajor.models import ChangeModel

from djzbar.utils.informix import do_sql

import re


class ChangeForm(forms.ModelForm):
    # Overrides this function so I can add custom validation
    def __init__(self, *args, **kwargs):
        super(ChangeForm, self).__init__(*args,**kwargs)

    def clean_student_id(self):
        data = self.cleaned_data['student_id']
        if not re.match(r'^(\d{5,7})$', data):
            raise forms.ValidationError('Must be 5-7 digits long')
        return data

    def clean_advisor(self):
        data = self.cleaned_data['advisor']
        # make sure there is something in data
        # so there wont be an error with the sql
        advisor_name = data.split(', ')
        if len(advisor_name) == 2:
            # try to find advisor id in database to see
            # if this id is for a valid advisor
            sql = '''
                SELECT
                    job_rec.id AS id
                FROM
                    job_rec
                INNER JOIN
                    id_rec
                ON
                    job_rec.id = id_rec.id
                WHERE
                    hrstat = 'FT'
                AND
                    TODAY BETWEEN
                        job_rec.beg_date
                    AND
                        NVL(job_rec.end_date, TODAY)
                AND
                    id_rec.firstname = "{}"
                AND
                    id_rec.lastname = "{}"
                '''.format(advisor_name[1], advisor_name[0])
            result = do_sql(
                sql, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
            )
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
