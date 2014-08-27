from django.db import models
from djzbar import settings
from djreggie import settings
from djzbar.utils.informix import do_sql
from sqlalchemy import create_engine


#My model with the fields I will find in the form
class Form(models.Model):
    
    #All my fields in the form are below
   # name = models.CharField(max_length=100, null=True, blank=True) #'max_length' is required in (most) all fields
    student_ID = models.CharField(max_length=7)
    consent = models.CharField(max_length = 9) #This renders as a select box
    
    def save(self):
        sql = '''INSERT INTO cc_stg_ferpadirectory (student_id, consent, datecreated)
        VALUES (%(student_ID)s, "%(consent)s", CURRENT)''' % (self.__dict__)
        do_sql(sql, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)
        sql2 = '''UPDATE profile_rec
                SET priv_code = '''
        if self.__dict__['consent'] == "NOCONSENT":
            sql2 += '"FERP"'
        else:
            sql2 += '""'
        sql2 += 'WHERE id = %s' % (self.__dict__['student_ID'])
        do_sql(sql2, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)