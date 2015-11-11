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
        insertSQL = '''INSERT INTO cc_stg_ferpadirectory (student_id, consent, datecreated)
        VALUES (%(student_ID)s, "%(consent)s", CURRENT)''' % (self.__dict__)
        do_sql(insertSQL, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)
        updateSQL = '''UPDATE profile_rec
                SET priv_code = '''
        if self.__dict__['consent'] == "NOCONSENT":
            updateSQL += '"FERP"'
        else:
            updateSQL += '""'
        updateSQL += 'WHERE id = %s' % (self.__dict__['student_ID'])
        do_sql(updateSQL, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)