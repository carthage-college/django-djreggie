#Need this
from django.db import models
from djzbar.settings import INFORMIX_EARL_TEST
from sqlalchemy import create_engine

#SQL Alchemy
engine = create_engine(INFORMIX_EARL_TEST)
connection = engine.connect()

#Majors
sql1 = "select * from major_table ORDER BY txt ASC"
major = connection.execute(sql1)
array1 = []
for row in major:
    array1.append((row['major'],row['txt']))   
CHOICES1 = tuple(array1)

#Minors
sql2 = "select * from minor_table ORDER BY txt ASC"
minor = connection.execute(sql2)
array2 = []
for row in minor:
    array2.append((row['minor'],row['txt']))   
CHOICES2 = tuple(array2)


# Create your models here.
'''
class Major(models.Model):
    unique_id = models.AutoField(primary_key=True)
    txt = models.CharField(max_length=100, choices=CHOICES1)
    class Meta:
        #db_table = 'changemajor_student_majors'
        ordering = ['txt']
    #How we see this model displayed
    def __unicode__(self):
        return self.txt
'''    
'''    
class Minor(models.Model):
    unique_id = models.AutoField(primary_key=True)
    txt = models.CharField(max_length=100, choices=CHOICES2)
    class Meta:
        #db_table = 'changemajor_student_minors'
        ordering = ['txt']
    #How we see this model displayed
    def __unicode__(self):
        return self.txt
'''
    
class Student(models.Model):
    
    #Fields in my form
    
    student_id = models.IntegerField(primary_key=True,max_length=7,blank=False) #Is the primary key of the form
    name = models.CharField(max_length=200,blank=False) #'blank=False' means the field is required
    
    YEAR_IN_SCHOOL = (
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
    )
    
    year = models.CharField("Year in school",max_length=2,blank=False,choices=YEAR_IN_SCHOOL) #Renders as a select field
    advisor = models.CharField(max_length=200, null=True, blank=True) #'null=True' means this value can display as null in the database table
    
    majors = models.CharField(max_length=100, choices=CHOICES1) #Defines a many to many (m2m) relationship with the model 'Major'
    minors = models.CharField(max_length=100, choices=CHOICES2, blank=True, null=True) #Defines a many to many (m2m) relationship with the model 'Minor'
    
    #How we see this model displayed
    def __unicode__(self):
        return self.name
        
    #Global options
    class Meta:
        ordering = ['majors', 'minors']

#Proxy class    
class ProxyStudent(Student):
    class Meta:
        proxy = True #Need this
        app_label = 'Registrar' #Header that the 'Student' model will display under the admin page
        verbose_name = 'Change Of Major/Minor/Advisor Form' #Name that will display in place of the form name
