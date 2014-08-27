from django.db import models
from djzbar import settings
from djreggie import settings
from djzbar.utils.informix import do_sql
from sqlalchemy import create_engine
#Each class is a model that will be turned into a form

class ConsentModel(models.Model):
    #This is where we declare the fields that will be used in our form
    full_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=7)
    Date = models.DateField(auto_now_add=True) #Auto now add makes the date equal the time the form was submitted
    
    def save(self): #this is for putting data in the database
        sql = '''SELECT COUNT(ferpafamily_no) AS cnt
                FROM cc_stg_ferpafamily
                WHERE student_id = %s''' % (self.__dict__['student_id'])
        entry = do_sql(sql, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL).first()['cnt']
        #check if an entry already exists in database. if it does then don't create a new one
        if not entry:
            sql2 = '''INSERT INTO cc_stg_ferpafamily (student_id, datecreated)
                    VALUES (%s, CURRENT)''' % (self.__dict__['student_id'])
            do_sql(sql2, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)
#This is our separate formset. A form that appears multiple times for cases such as entering multiple family members

class ParentForm(models.Model): 
    form = models.IntegerField()
    CHOICES = ( #Here we make some choices that will be assigned to a field
        ("ACADEMIC", 'Academic Records'),
        ("FINANCIAL", 'Financial Records'),
        ("BOTH", 'I would like to share both'),
        ("NEITHER", 'I would like to share neither'),
    )
    share = models.CharField(choices=CHOICES, max_length=200)    #This is the field we assign them to
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=16)
    email = models.EmailField()
    CHOICES2 = (    #More choices
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
    relation = models.CharField(choices=CHOICES2, max_length=20) #Stick those choices in here