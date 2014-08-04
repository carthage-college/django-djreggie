from django.db import models
from djzbar.settings import INFORMIX_EARL_TEST
from sqlalchemy import create_engine

engine = create_engine(INFORMIX_EARL_TEST)
connection = engine.connect()

#My model with the fields I will find in the form
class Form(models.Model):
    
    #All my fields in the form are below
   # name = models.CharField(max_length=100, null=True, blank=True) #'max_length' is required in (most) all fields
    student_ID = models.CharField(max_length=7)
    consent = models.CharField(max_length = 9) #This renders as a select box
    
    def save(self):
        engine = create_engine(INFORMIX_EARL_TEST) #This is how we save to the database
        connection = engine.connect()
        sql = '''INSERT INTO cc_stg_ferpadirectory (student_id, consent, datecreated)
        VALUES (%(student_ID)s, "%(consent)s", CURRENT)''' % (self.__dict__)
        connection.execute(sql)