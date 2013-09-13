#Need this
from django.db import models



# Create your models here.

class Major(models.Model):
    txt = models.CharField(db_column = 'txt')
    major = models.CharField(db_column = 'major')
    class Meta:
        db_table = 'major_table'
    #How we see this model displayed
    def __unicode__(self):
        return self.txt


class Minor(models.Model):
    txt = models.CharField(db_column = 'txt')
    class Meta:
        db_table = 'minor_table'
    #How we see this model displayed
    def __unicode__(self):
        return self.txt

    
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
    
    majors = models.ManyToManyField(Major) #Defines a many to many (m2m) relationship with the model 'Major'
    minors = models.ManyToManyField(Minor, blank=True, null=True) #Defines a many to many (m2m) relationship with the model 'Minor'
    
    #How we see this model displayed
    def __unicode__(self):
        return self.name
        

#Proxy class    
class ProxyStudent(Student):
    class Meta:
        proxy = True #Need this
        app_label = 'Registrar' #Header that the 'Student' model will display under the admin page
        verbose_name = 'Change Of Major/Minor/Advisor Form' #Name that will display in place of the form name
