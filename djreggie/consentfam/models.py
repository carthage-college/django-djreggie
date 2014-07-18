from django.db import models
from djzbar.settings import INFORMIX_EARL_TEST
from sqlalchemy import create_engine
#Each class is a model that will be turned into a form

class ConsentModel(models.Model):
    #CHOICES1 = (
    #    ("ACCEPT", 'I agree with the previous statement.'),
    #)
    full_name = models.CharField(max_length=100, verbose_name='Name')
    student_id = models.CharField(max_length=7,
                                             verbose_name='Student ID')
    Date = models.DateField(auto_now_add=True)
    phone = models.CharField(max_length=14)
    email = models.EmailField()

    def __unicode__(self):
        return self.Full_Name_of_Student
    
    def save(self):
        engine = create_engine(INFORMIX_EARL_TEST)
        connection = engine.connect()
        sql = '''INSERT INTO cc_stg_ferpafamily (student_id, datecreated)
                VALUES (%s, TODAY)''' % (self.__dict__['student_id'])
        connection.execute(sql)

class ParentForm(models.Model):
    form = models.IntegerField()
    CHOICES = (
        ("ACADEMIC", 'Academic Records'),
        ("FINANCIAL", 'Financial Records'),
        ("BOTH", 'I would like to share both'),
        ("NEITHER", 'I would like to share neither'),
        ("OLD", "I would like to keep my old sharing settings"),
    )
    share = models.CharField(choices=CHOICES, max_length=200)    
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=16)
    email = models.EmailField()
    CHOICES2 = (    
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
    relation = models.CharField(choices=CHOICES2,
                                max_length=20,
                                verbose_name='Relation')